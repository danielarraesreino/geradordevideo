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
                    <CardTitle className="text-lg font-bold">Roteiro Principal</CardTitle>
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
                <Textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    placeholder="Escreva o roteiro aqui..."
                    className="flex-1 font-mono text-sm leading-relaxed resize-none bg-white border-blue-100 focus-visible:ring-blue-400"
                />
                <Button
                    onClick={() => onSave(content)}
                    disabled={isLoading || isOverLimit}
                    className="bg-blue-600 hover:bg-blue-700 w-full"
                >
                    {isLoading ? "Salvando..." : "Salvar Alterações"}
                </Button>
            </CardContent>
        </Card>
    );
}
