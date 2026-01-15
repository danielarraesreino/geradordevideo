"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Smile, Type, Plus, X, Share2, Info } from "lucide-react";

export interface StickerOverlay {
    id: string;
    type: "image" | "text";
    content: string;
    position: { x: number; y: number };
    style?: React.CSSProperties;
}

interface StickerManagerProps {
    activeStickers: StickerOverlay[];
    onAddSticker: (sticker: StickerOverlay) => void;
    onRemoveSticker: (id: string) => void;
}

const PRESET_STICKERS = [
    { id: "s1", label: "Direito ao Teto", icon: "🏠" },
    { id: "s2", label: "A Rua Tem Voz", icon: "🗣️" },
    { id: "s3", label: "PDI Campinas", icon: "📍" },
    { id: "s4", label: "Dignidade Já", icon: "✊" },
    { id: "s5", label: "Vizinhança Solidária", icon: "🤝" },
];

export function StickerManager({ activeStickers, onAddSticker, onRemoveSticker }: StickerManagerProps) {
    const [customText, setCustomText] = useState("");
    const [textColor, setTextColor] = useState("#ffffff");
    const [bgColor, setBgColor] = useState("#2563eb");

    const handleAddPreset = (preset: typeof PRESET_STICKERS[0]) => {
        onAddSticker({
            id: `preset-${Date.now()}`,
            type: "text",
            content: `${preset.icon} ${preset.label}`,
            position: { x: 10, y: 10 },
            style: {
                backgroundColor: "#ffffff",
                color: "#1e40af",
                padding: "4px 10px",
                borderRadius: "20px",
                fontWeight: "bold",
                fontSize: "12px",
                boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
                border: "1px solid #bfdbfe"
            }
        });
    };

    const handleAddText = () => {
        if (!customText.trim()) return;
        onAddSticker({
            id: `text-${Date.now()}`,
            type: "text",
            content: customText,
            position: { x: 20, y: 20 },
            style: {
                backgroundColor: bgColor,
                color: textColor,
                padding: "8px 16px",
                borderRadius: "4px",
                fontWeight: "bold",
                fontSize: "16px",
                boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
                transform: "rotate(-2deg)"
            }
        });
        setCustomText("");
    };

    return (
        <Card className="h-full border-0 shadow-none bg-transparent">
            <CardHeader className="px-0 pt-0">
                <CardTitle className="text-lg font-bold flex items-center gap-2">
                    <Share2 className="w-5 h-5 text-blue-600" /> Overlays Sociais
                </CardTitle>
            </CardHeader>
            <CardContent className="p-0 space-y-6">
                {/* Ativos */}
                <div className="space-y-3">
                    <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">Overlays na Cena</p>
                    <div className="flex flex-wrap gap-2 min-h-[40px] p-2 bg-gray-50 rounded-lg border border-dashed border-gray-200">
                        {activeStickers.length === 0 ? (
                            <p className="text-[10px] text-gray-400 italic">Nenhum sticker ativo</p>
                        ) : (
                            activeStickers.map((s) => (
                                <Badge key={s.id} variant="secondary" className="gap-1.5 px-2 py-1 bg-white border border-blue-100 text-blue-800">
                                    {s.content}
                                    <X className="w-3 h-3 cursor-pointer hover:text-red-500" onClick={() => onRemoveSticker(s.id)} />
                                </Badge>
                            ))
                        )}
                    </div>
                </div>

                {/* Stickers Preset */}
                <div className="space-y-3">
                    <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">Presets Pop Rua</p>
                    <div className="grid grid-cols-2 gap-2">
                        {PRESET_STICKERS.map((p) => (
                            <Button
                                key={p.id}
                                variant="outline"
                                size="sm"
                                className="h-9 justify-start gap-2 text-xs font-medium border-blue-50 hover:bg-blue-50 hover:border-blue-200 transition-all"
                                onClick={() => handleAddPreset(p)}
                            >
                                <span className="text-sm">{p.icon}</span>
                                {p.label}
                            </Button>
                        ))}
                    </div>
                </div>

                {/* Custom Text */}
                <div className="space-y-3">
                    <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">Sticker de Texto Personalizado</p>
                    <div className="space-y-2">
                        <Input
                            placeholder="Digite sua mensagem de impacto..."
                            value={customText}
                            onChange={(e) => setCustomText(e.target.value)}
                            className="text-xs h-9"
                        />
                        <div className="flex gap-2">
                            <div className="flex-1 flex gap-2">
                                <input
                                    type="color"
                                    value={bgColor}
                                    onChange={(e) => setBgColor(e.target.value)}
                                    className="w-8 h-9 p-0 border-0 bg-transparent cursor-pointer"
                                    title="Fundo"
                                />
                                <input
                                    type="color"
                                    value={textColor}
                                    onChange={(e) => setTextColor(e.target.value)}
                                    className="w-8 h-9 p-0 border-0 bg-transparent cursor-pointer"
                                    title="Texto"
                                />
                            </div>
                            <Button size="sm" className="h-9 gap-2" onClick={handleAddText}>
                                <Plus className="w-3.5 h-3.5" /> Adicionar
                            </Button>
                        </div>
                    </div>
                </div>

                <div className="bg-amber-50 border border-amber-100 rounded-lg p-3 flex gap-2">
                    <Info className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                    <p className="text-[10px] text-amber-800 leading-tight">
                        Os stickers ajudam a contextualizar a denúncia ou conquista nas redes sociais, aumentando o engajamento e a visibilidade política.
                    </p>
                </div>
            </CardContent>
        </Card>
    );
}
