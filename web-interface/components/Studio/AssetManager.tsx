"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Image as ImageIcon, Check, Plus } from "lucide-react";

interface Asset {
    name: string;
    url: string;
}

interface AssetManagerProps {
    onSelectScene: (index: number, asset: Asset) => void;
    selectedAssets: (Asset | null)[];
}

export function AssetManager({ onSelectScene, selectedAssets }: AssetManagerProps) {
    const [availableAssets, setAvailableAssets] = useState<Asset[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function fetchAssets() {
            try {
                const response = await fetch("/api/assets");
                const data = await response.json();
                setAvailableAssets(data);
            } catch (error) {
                console.error("Failed to fetch assets:", error);
            } finally {
                setIsLoading(false);
            }
        }
        fetchAssets();
    }, []);

    return (
        <Card className="h-full border-0 shadow-none bg-transparent">
            <CardHeader className="px-0 pt-0">
                <CardTitle className="text-lg font-bold flex items-center gap-2">
                    <ImageIcon className="w-5 h-5" /> Assets Visuais
                </CardTitle>
            </CardHeader>
            <CardContent className="p-0 space-y-6">
                {/* Cenas Atuais */}
                <div className="space-y-3">
                    <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">Timeline de Cenas</p>
                    <div className="grid grid-cols-5 gap-2">
                        {[0, 1, 2, 3, 4].map((idx) => (
                            <div
                                key={idx}
                                className={`aspect-square rounded-md border-2 border-dashed flex items-center justify-center overflow-hidden transition-all relative ${selectedAssets[idx] ? "border-blue-400" : "border-gray-200 hover:border-gray-300"
                                    }`}
                            >
                                {selectedAssets[idx] ? (
                                    <>
                                        <img src={selectedAssets[idx]!.url} className="w-full h-full object-cover" alt={`Cena ${idx + 1}`} />
                                        <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
                                            <Button variant="ghost" size="sm" className="text-white h-7 w-7 p-0 rounded-full" onClick={() => onSelectScene(idx, null as any)}>
                                                ×
                                            </Button>
                                        </div>
                                    </>
                                ) : (
                                    <span className="text-[10px] font-bold text-gray-300">{idx + 1}</span>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Galeria */}
                <div className="space-y-3">
                    <div className="flex justify-between items-center">
                        <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">Banco de Imagens</p>
                        <Button variant="ghost" size="sm" className="h-6 text-[10px] px-2 text-blue-600">Upload +</Button>
                    </div>

                    <div className="grid grid-cols-2 gap-2 h-[300px] overflow-y-auto pr-2 custom-scrollbar">
                        {isLoading ? (
                            <div className="col-span-2 py-8 text-center text-sm text-gray-400">Carregando...</div>
                        ) : availableAssets.length === 0 ? (
                            <div className="col-span-2 py-8 text-center text-sm text-gray-400">Nenhuma imagem encontrada</div>
                        ) : (
                            availableAssets.map((asset) => (
                                <div
                                    key={asset.name}
                                    className="group relative aspect-video rounded-md overflow-hidden bg-gray-100 cursor-pointer border border-transparent hover:border-blue-400 transition-all"
                                    onClick={() => {
                                        // Adicionar na primeira cena vazia
                                        const emptyIdx = selectedAssets.findIndex(a => a === null);
                                        if (emptyIdx !== -1) onSelectScene(emptyIdx, asset);
                                    }}
                                >
                                    <img src={asset.url} className="w-full h-full object-cover" alt={asset.name} />
                                    <div className="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition-colors" />
                                    <div className="absolute top-1 right-1">
                                        <div className="bg-white/90 p-1 rounded-full shadow-sm opacity-0 group-hover:opacity-100 transition-opacity">
                                            <Plus className="w-3 h-3 text-blue-600" />
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
