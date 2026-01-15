"use client";

import { useState, useEffect, use } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScriptEditor } from "@/components/Studio/ScriptEditor";
import { AssetManager } from "@/components/Studio/AssetManager";
import { VideoPreview } from "@/components/Studio/VideoPreview";
import { SubtitleEditor } from "@/components/Studio/SubtitleEditor";
import { StickerManager, type StickerOverlay } from "@/components/Studio/StickerManager";
import { ChevronLeft, Share2, Settings, Info } from "lucide-react";
import { toast } from "sonner";

interface Asset {
    name: string;
    url: string;
}

interface Story {
    id: string;
    NOME_FICTICIO: string;
    tema_narrativo: string;
    script?: string;
}

export default function StudioPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = use(params);
    const [story, setStory] = useState<Story | null>(null);
    const [selectedAssets, setSelectedAssets] = useState<(Asset | null)[]>([null, null, null, null, null]);
    const [activeStickers, setActiveStickers] = useState<StickerOverlay[]>([]);
    const [rightPanel, setRightPanel] = useState<"assets" | "overlays">("assets");
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);

    useEffect(() => {
        async function fetchStory() {
            try {
                const response = await fetch(`/api/stories/${id}`);
                if (!response.ok) throw new Error("Failed to fetch story");
                const data = await response.json();
                setStory(data);
            } catch (error) {
                console.error(error);
                toast.error("Erro ao carregar história");
            } finally {
                setIsLoading(false);
            }
        }
        fetchStory();
    }, [id]);

    const handleSaveScript = async (content: string) => {
        setIsSaving(true);
        try {
            const response = await fetch(`/api/stories/${id}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ content }),
            });
            if (!response.ok) throw new Error("Failed to save script");
            toast.success("Roteiro salvo com sucesso!");
        } catch (error) {
            console.error(error);
            toast.error("Erro ao salvar roteiro");
        } finally {
            setIsSaving(false);
        }
    };

    const handleSelectAsset = (index: number, asset: Asset) => {
        const newAssets = [...selectedAssets];
        newAssets[index] = asset;
        setSelectedAssets(newAssets);
    };

    const handleAddSticker = (sticker: StickerOverlay) => {
        setActiveStickers([...activeStickers, sticker]);
    };

    const handleRemoveSticker = (stickerId: string) => {
        setActiveStickers(activeStickers.filter(s => s.id !== stickerId));
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-50">
                <div className="flex flex-col items-center gap-4">
                    <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                    <p className="text-sm font-medium text-gray-500">Iniciando Studio...</p>
                </div>
            </div>
        );
    }

    if (!story) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 gap-4">
                <p className="text-gray-500">História não encontrada.</p>
                <Link href="/">
                    <Button variant="outline">Voltar para o Painel</Button>
                </Link>
            </div>
        );
    }

    return (
        <div className="flex flex-col h-screen bg-gray-50 overflow-hidden">
            {/* Header */}
            <header className="h-14 border-b bg-white flex items-center justify-between px-6 shrink-0">
                <div className="flex items-center gap-4">
                    <Link href="/">
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                            <ChevronLeft className="w-4 h-4" />
                        </Button>
                    </Link>
                    <div className="h-6 w-[1px] bg-gray-200" />
                    <div>
                        <h1 className="text-sm font-bold flex items-center gap-2">
                            Studio: <span className="text-blue-600">{story.NOME_FICTICIO}</span>
                        </h1>
                        <p className="text-[10px] text-gray-500 font-medium uppercase tracking-tight">{story.tema_narrativo}</p>
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    <Button variant="ghost" size="sm" className="h-8 text-xs gap-1.5">
                        <Share2 className="w-3.5 h-3.5" /> Compartilhar
                    </Button>
                    <Button variant="ghost" size="sm" className="h-8 text-xs gap-1.5">
                        <Settings className="w-3.5 h-3.5" /> Config
                    </Button>
                    <div className="w-[1px] h-4 bg-gray-200 mx-1" />
                    <Button className="bg-blue-600 hover:bg-blue-700 h-8 text-xs px-4 font-bold shadow-blue-200 shadow-lg">
                        Exportar Projeto
                    </Button>
                </div>
            </header>

            {/* Main Studio Area */}
            <main className="flex-1 flex overflow-hidden p-6 gap-6">
                {/* Left: Script Editor */}
                <div className="w-[350px] shrink-0">
                    <ScriptEditor
                        initialContent={story.script || ""}
                        onSave={handleSaveScript}
                        isLoading={isSaving}
                    />
                </div>

                {/* Center: Video Preview & Subtitles */}
                <div className="flex-1 flex flex-col gap-6 overflow-y-auto pr-2 custom-scrollbar">
                    <VideoPreview scenes={selectedAssets} stickers={activeStickers} />

                    <div className="grid grid-cols-2 gap-6">
                        <SubtitleEditor />
                        <div className="bg-white rounded-xl border border-blue-100 p-6 shadow-sm">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="text-sm font-bold flex items-center gap-2">
                                    <Info className="w-4 h-4 text-blue-500" /> Contexto do Projeto
                                </h3>
                                <Badge variant="secondary" className="bg-blue-50 font-mono text-[10px]">VER: 2026.01.15</Badge>
                            </div>
                            <p className="text-xs text-gray-600 leading-relaxed">
                                Este vídeo utiliza a técnica **Viral ST** focado no eixo PDI de {story.tema_narrativo}.
                                A estética aplicada é o **Realismo Sóbrio**, garantindo dignidade na representação e impacto visual
                                direcionado a políticas públicas em Campinas.
                            </p>
                        </div>
                    </div>
                </div>

                {/* Right: Asset & Overlay Manager */}
                <div className="w-[400px] shrink-0 flex flex-col gap-4">
                    <div className="flex bg-white p-1 rounded-lg border border-blue-100 shadow-sm">
                        <Button
                            variant={rightPanel === "assets" ? "default" : "ghost"}
                            size="sm"
                            className="flex-1 gap-2"
                            onClick={() => setRightPanel("assets")}
                        >
                            Assets
                        </Button>
                        <Button
                            variant={rightPanel === "overlays" ? "default" : "ghost"}
                            size="sm"
                            className="flex-1 gap-2"
                            onClick={() => setRightPanel("overlays")}
                        >
                            Overlays
                        </Button>
                    </div>

                    <div className="flex-1 overflow-y-auto">
                        {rightPanel === "assets" ? (
                            <AssetManager
                                selectedAssets={selectedAssets}
                                onSelectScene={handleSelectAsset}
                            />
                        ) : (
                            <StickerManager
                                activeStickers={activeStickers}
                                onAddSticker={handleAddSticker}
                                onRemoveSticker={handleRemoveSticker}
                            />
                        )}
                    </div>
                </div>
            </main>

            {/* Footer / Status Bar */}
            <footer className="h-8 border-t bg-gray-900 flex items-center justify-between px-6 shrink-0 text-[10px] text-white/50 font-mono">
                <div className="flex gap-4">
                    <span>GPU: RENDER_IDLE</span>
                    <span className="text-emerald-500">SYNC_OK</span>
                </div>
                <div className="flex gap-4">
                    <span>LOCAL: /studio/{id}</span>
                    <span>STORY_ID: {id}</span>
                </div>
            </footer>
        </div>
    );
}
