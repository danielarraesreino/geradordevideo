"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Type, Clock, Plus, Trash2 } from "lucide-react";

interface Subtitle {
    id: string;
    text: string;
    start: string;
    end: string;
}

export function SubtitleEditor() {
    const [subtitles, setSubtitles] = useState<Subtitle[]>([
        { id: "1", text: "Eu já vendi pente quebrado para não morrer de fome...", start: "00:00", end: "00:05" },
        { id: "2", text: "E descobri que a rua não te tira apenas o teto.", start: "00:05", end: "00:10" },
    ]);

    const addSubtitle = () => {
        const lastSub = subtitles[subtitles.length - 1];
        const newId = (parseInt(lastSub?.id || "0") + 1).toString();
        setSubtitles([...subtitles, { id: newId, text: "", start: "00:00", end: "00:00" }]);
    };

    const removeSubtitle = (id: string) => {
        setSubtitles(subtitles.filter(s => s.id !== id));
    };

    const updateSubtitle = (id: string, field: keyof Subtitle, value: string) => {
        setSubtitles(subtitles.map(s => s.id === id ? { ...s, [field]: value } : s));
    };

    return (
        <Card className="border-blue-100 shadow-sm bg-white">
            <CardHeader className="pb-3 border-b border-gray-50 flex flex-row items-center justify-between">
                <CardTitle className="text-sm font-bold flex items-center gap-2">
                    <Type className="w-4 h-4 text-blue-500" /> Editor de Legendas
                </CardTitle>
                <Button variant="ghost" size="sm" className="h-7 text-[10px] gap-1 text-blue-600" onClick={addSubtitle}>
                    <Plus className="w-3 h-3" /> Nova Linha
                </Button>
            </CardHeader>
            <CardContent className="p-4 space-y-3 max-h-[300px] overflow-y-auto custom-scrollbar">
                {subtitles.map((sub) => (
                    <div key={sub.id} className="flex gap-2 items-start group">
                        <div className="flex flex-col gap-1 w-20 shrink-0">
                            <div className="flex items-center gap-1 bg-gray-50 p-1 rounded border text-[10px] font-mono">
                                <Clock className="w-3 h-3 text-gray-400" /> {sub.start}
                            </div>
                            <div className="flex items-center gap-1 bg-gray-50 p-1 rounded border text-[10px] font-mono">
                                <Clock className="w-3 h-3 text-gray-400" /> {sub.end}
                            </div>
                        </div>
                        <Input
                            value={sub.text}
                            onChange={(e) => updateSubtitle(sub.id, "text", e.target.value)}
                            className="h-12 text-xs bg-white border-blue-50 focus-visible:ring-blue-200"
                            placeholder="Digite o texto da legenda..."
                        />
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-12 w-8 text-gray-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                            onClick={() => removeSubtitle(sub.id)}
                        >
                            <Trash2 className="w-4 h-4" />
                        </Button>
                    </div>
                ))}
            </CardContent>
        </Card>
    );
}
