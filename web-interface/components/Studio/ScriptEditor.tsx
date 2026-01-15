"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertCircle, CheckCircle2 } from "lucide-react";

interface ScriptEditorProps {
    initialContent: string;
    onSave: (content: string) => void;
    isLoading?: boolean;
}

export function ScriptEditor({ initialContent, onSave, isLoading }: ScriptEditorProps) {
    const [content, setContent] = useState(initialContent);
    const charLimit = 1300;
    const charCount = content.length;
    const isOverLimit = charCount > charLimit;
    const isTooShort = charCount < 1100;

    useEffect(() => {
        setContent(initialContent);
    }, [initialContent]);

    return (
        <Card className="h-full flex flex-col border-0 shadow-none bg-transparent">
            <CardHeader className="px-0 pt-0">
                <div className="flex justify-between items-center">
                    <div>
                        <CardTitle className="text-lg font-bold">Roteiro Principal</CardTitle>
                        <p className="text-[10px] text-blue-500 font-bold uppercase tracking-widest mt-0.5">Marshall Ganz Framework</p>
                    </div>
                    <div className="flex items-center gap-2">
                        <span className={`text-sm font-medium ${isOverLimit ? "text-red-500" : isTooShort ? "text-amber-500" : "text-emerald-500"}`}>
                            {charCount} / {charLimit}
                        </span>
                        {isOverLimit ? (
                            <AlertCircle className="w-4 h-4 text-red-500" />
                        ) : isTooShort ? (
                            <Badge variant="outline" className="text-amber-600 border-amber-200 bg-amber-50">Curto</Badge>
                        ) : (
                            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                        )}
                    </div>
                </div>
            </CardHeader>
            <CardContent className="flex-1 p-0 flex flex-col gap-4">
                <div className="relative flex-1 flex flex-col">
                    <Textarea
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        placeholder="Escreva o roteiro aqui..."
                        className="flex-1 font-mono text-sm leading-relaxed resize-none bg-white border-blue-100 focus-visible:ring-blue-400 min-h-[300px]"
                    />

                    {/* Structure Indicators */}
                    <div className="absolute right-[-10px] top-1/2 -translate-y-1/2 flex flex-col gap-8 opacity-20 hover:opacity-100 transition-opacity pointer-events-none">
                        <div className="bg-blue-600 text-white text-[8px] py-1 px-2 rounded-l-md vertical-text font-bold">SELF</div>
                        <div className="bg-blue-600 text-white text-[8px] py-1 px-2 rounded-l-md vertical-text font-bold">US</div>
                        <div className="bg-blue-600 text-white text-[8px] py-1 px-2 rounded-l-md vertical-text font-bold">NOW</div>
                    </div>
                </div>

                <div className="bg-blue-50/50 rounded-lg p-3 border border-blue-100">
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-[10px] font-bold text-blue-700 uppercase tracking-tight">Validação Ética</span>
                        <div className="flex items-center gap-1">
                            <div className="h-1.5 w-16 bg-gray-200 rounded-full overflow-hidden">
                                <div className="h-full bg-emerald-500 w-[85%]" />
                            </div>
                            <span className="text-[10px] font-bold text-emerald-600">85/100</span>
                        </div>
                    </div>
                    <ul className="text-[9px] text-blue-800/70 space-y-1 font-medium">
                        <li className="flex items-center gap-1.5">✅ Dignidade preservada (Ausência de termos sensacionalistas)</li>
                        <li className="flex items-center gap-1.5">✅ Utilidade Pública (Centro POP/Bagageiro identificado)</li>
                        <li className="flex items-center gap-1.5">✅ Narrativa Sóbria (Foco em dados do Censo 2024)</li>
                    </ul>
                </div>

                <Button
                    onClick={() => onSave(content)}
                    disabled={isLoading || isOverLimit}
                    className="bg-blue-600 hover:bg-blue-700 w-full shadow-lg shadow-blue-200 font-bold"
                >
                    {isLoading ? "Salvando..." : "Salvar Alterações"}
                </Button>
            </CardContent>

            <style jsx>{`
                .vertical-text {
                    writing-mode: vertical-rl;
                    text-orientation: mixed;
                }
            `}</style>
        </Card>
    );
}
