"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Play, Pause, SkipBack, SkipForward, Wand2, Type, Smartphone, Monitor } from "lucide-react";
import { StickerOverlay } from "./StickerManager";

interface Asset {
    name: string;
    url: string;
}

interface VideoPreviewProps {
    scenes: (Asset | null)[];
    stickers?: StickerOverlay[];
}

export function VideoPreview({ scenes, stickers = [] }: VideoPreviewProps) {
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentSceneIdx, setCurrentSceneIdx] = useState(0);
    const [filter, setFilter] = useState<"none" | "grayscale" | "sepia" | "contrast">("none");
    const [showSubtitles, setShowSubtitles] = useState(true);
    const [aspectRatio, setAspectRatio] = useState<"16:9" | "9:16">("16:9");

    const filters = {
        none: "",
        grayscale: "grayscale(100%) brightness(0.9) contrast(1.2)",
        sepia: "sepia(50%) brightness(0.8) contrast(1.1)",
        contrast: "contrast(1.5) brightness(0.8)"
    };

    return (
        <div className="space-y-4">
            <div className={`mx-auto transition-all duration-500 overflow-hidden bg-black border-blue-900/50 shadow-2xl relative group ${aspectRatio === "16:9" ? "aspect-video w-full" : "aspect-[9/16] h-[500px]"
                }`}>
                <Card className="w-full h-full border-0 bg-transparent rounded-none relative overflow-hidden">
                    {scenes[currentSceneIdx] ? (
                        <img
                            src={scenes[currentSceneIdx]!.url}
                            className="w-full h-full object-cover transition-all duration-700"
                            style={{ filter: filters[filter] }}
                            alt="Preview"
                        />
                    ) : (
                        <div className="w-full h-full flex flex-col items-center justify-center text-gray-600 bg-gray-950">
                            <ImageIcon className="w-12 h-12 mb-2 opacity-20" />
                            <p className="text-xs font-mono uppercase tracking-widest opacity-40">Aguardando Asset {currentSceneIdx + 1}</p>
                        </div>
                    )}

                    {/* Stickers Layer */}
                    <div className="absolute inset-0 pointer-events-none">
                        {stickers.map((s) => (
                            <div
                                key={s.id}
                                className="absolute"
                                style={{
                                    left: `${s.position.x}%`,
                                    top: `${s.position.y}%`,
                                    ...s.style
                                }}
                            >
                                {s.content}
                            </div>
                        ))}
                    </div>

                    {/* Subtitles Overlay */}
                    {showSubtitles && (
                        <div className={`absolute left-0 right-0 text-center px-8 pointer-events-none ${aspectRatio === "9:16" ? "bottom-20" : "bottom-6"}`}>
                            <p className="inline-block bg-black/60 text-white px-4 py-1 rounded text-sm font-medium border border-white/10 backdrop-blur-sm">
                                Legenda sincronizada aparece aqui...
                            </p>
                        </div>
                    )}

                    {/* Hud Overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-4">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <Button size="icon" variant="ghost" className="text-white hover:bg-white/20" onClick={() => setIsPlaying(!isPlaying)}>
                                    {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5 fill-current" />}
                                </Button>
                                <div className="flex items-center gap-1">
                                    <Button size="icon" variant="ghost" className="text-white/70 h-8 w-8" onClick={() => setCurrentSceneIdx(Math.max(0, currentSceneIdx - 1))}>
                                        <SkipBack className="w-4 h-4" />
                                    </Button>
                                    <span className="text-[10px] font-mono text-white/50 w-12 text-center">
                                        0{currentSceneIdx + 1} / 05
                                    </span>
                                    <Button size="icon" variant="ghost" className="text-white/70 h-8 w-8" onClick={() => setCurrentSceneIdx(Math.min(4, currentSceneIdx + 1))}>
                                        <SkipForward className="w-4 h-4" />
                                    </Button>
                                </div>
                            </div>

                            <div className="flex gap-2">
                                <Badge variant="outline" className="bg-blue-500/20 text-blue-300 border-blue-500/30 text-[10px] uppercase">
                                    {aspectRatio} HQ
                                </Badge>
                            </div>
                        </div>
                    </div>
                </Card>
            </div>

            {/* Editor Controls */}
            <div className="flex justify-between items-center bg-white p-3 rounded-lg border border-blue-100 shadow-sm">
                <div className="flex items-center gap-4">
                    <div className="space-y-1">
                        <p className="text-[10px] uppercase tracking-wider font-bold text-gray-400">Layout</p>
                        <div className="flex gap-1">
                            <Button
                                variant="outline"
                                size="sm"
                                className={`h-7 w-8 p-0 ${aspectRatio === "16:9" ? "bg-blue-50 border-blue-200" : ""}`}
                                onClick={() => setAspectRatio("16:9")}
                                title="Widescreen (YouTube/TV)"
                            >
                                <Monitor className="w-4 h-4" />
                            </Button>
                            <Button
                                variant="outline"
                                size="sm"
                                className={`h-7 w-8 p-0 ${aspectRatio === "9:16" ? "bg-blue-50 border-blue-200" : ""}`}
                                onClick={() => setAspectRatio("9:16")}
                                title="Social (TikTok/Reels)"
                            >
                                <Smartphone className="w-4 h-4" />
                            </Button>
                        </div>
                    </div>

                    <div className="h-8 w-[1px] bg-gray-100 mx-2" />

                    <div className="space-y-1">
                        <p className="text-[10px] uppercase tracking-wider font-bold text-gray-400">Estética / Filtro</p>
                        <div className="flex gap-1">
                            {(["none", "grayscale", "sepia", "contrast"] as const).map((f) => (
                                <button
                                    key={f}
                                    onClick={() => setFilter(f)}
                                    className={`h-6 w-6 rounded-full border-2 transition-all ${filter === f ? "border-blue-600 scale-110 shadow-sm" : "border-gray-200 hover:border-gray-300"
                                        }`}
                                    style={{
                                        backgroundColor: f === "none" ? "#ddd" :
                                            f === "grayscale" ? "#888" :
                                                f === "sepia" ? "#964B00" : "#333"
                                    }}
                                    title={f}
                                />
                            ))}
                        </div>
                    </div>

                    <div className="h-8 w-[1px] bg-gray-100 mx-2" />

                    <div className="space-y-1">
                        <p className="text-[10px] uppercase tracking-wider font-bold text-gray-400">Interface</p>
                        <div className="flex gap-2">
                            <Button
                                variant="outline"
                                size="sm"
                                className={`h-7 text-[10px] gap-1 ${showSubtitles ? "bg-blue-50 border-blue-200 text-blue-700" : ""}`}
                                onClick={() => setShowSubtitles(!showSubtitles)}
                            >
                                <Type className="w-3 h-3" /> Legendas
                            </Button>
                            <Button variant="outline" size="sm" className="h-7 text-[10px] gap-1">
                                <Wand2 className="w-3 h-3" /> Auto-Enhance
                            </Button>
                        </div>
                    </div>
                </div>

                <Button className="bg-emerald-600 hover:bg-emerald-700 h-9 font-bold">
                    Renderizar Vídeo Final
                </Button>
            </div>
        </div>
    );
}

// Missing icon import from previous copy-paste thought
import { Image as ImageIcon } from "lucide-react";
