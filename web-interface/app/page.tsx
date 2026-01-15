import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { FileVideo, PenTool, LayoutTemplate, History } from "lucide-react"

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="px-4 lg:px-6 h-14 flex items-center border-b bg-gray-50/50">
        <Link className="flex items-center justify-center font-bold text-xl" href="#">
          <span className="text-blue-600 mr-2">Vector</span>Galaxy
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link className="text-sm font-medium hover:underline underline-offset-4" href="#">
            Projetos
          </Link>
        </nav>
      </header>
      <main className="flex-1 p-8 bg-gray-50">
        <div className="max-w-6xl mx-auto space-y-8">

          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Studio Pop Rua</h1>
              <p className="text-muted-foreground mt-2">Gerencie e produza seus vídeos de impacto social.</p>
            </div>
            <Button className="bg-blue-600 hover:bg-blue-700">
              + Nova História (CLI)
            </Button>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {/* Card de Projeto Ativo */}
            <Link href="/studio/005">
              <Card className="hover:shadow-md transition-shadow cursor-pointer border-blue-200 bg-blue-50/30">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <Badge variant="outline" className="bg-emerald-100 text-emerald-800 border-emerald-200">Em Produção</Badge>
                    <span className="text-xs text-gray-500">ID: #005</span>
                  </div>
                  <CardTitle className="mt-2 text-gray-900">Rogério (Saúde)</CardTitle>
                  <CardDescription>Tema: Apartação Social</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex gap-2 text-sm text-gray-600 mb-4">
                    <div className="flex items-center"><PenTool className="w-3 h-3 mr-1" /> Roteiro</div>
                    <div className="flex items-center"><LayoutTemplate className="w-3 h-3 mr-1" /> Assets</div>
                  </div>
                  <Button className="w-full" variant="outline">Abrir Editor</Button>
                </CardContent>
              </Card>
            </Link>

            {/* Card de Projeto Concluído */}
            <Link href="/studio/002">
              <Card className="hover:shadow-md transition-shadow opacity-75 bg-white cursor-pointer">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <Badge variant="secondary">Concluído</Badge>
                    <span className="text-xs text-gray-500">ID: #002</span>
                  </div>
                  <CardTitle className="mt-2 text-gray-900">Maria (Financeiro)</CardTitle>
                  <CardDescription>Tema: Exclusão Bancária</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full" variant="ghost">Ver Vídeo</Button>
                </CardContent>
              </Card>
            </Link>

            {/* Card Placeholder */}
            <Card className="border-dashed flex flex-col items-center justify-center p-6 text-gray-400 hover:bg-gray-100/50 cursor-pointer transition-colors bg-white">
              <FileVideo className="w-10 h-10 mb-2 opacity-50" />
              <p>Importar Novo Caso</p>
            </Card>

          </div>

          <div className="mt-12">
            <h2 className="text-xl font-semibold mb-4 flex items-center text-gray-900">
              <History className="w-5 h-5 mr-2" /> Atividade Recente
            </h2>
            <div className="bg-white rounded-lg border shadow-sm p-4 text-sm space-y-3">
              <div className="flex justify-between py-2 border-b">
                <span className="text-gray-900">Renderização Final (#005)</span>
                <span className="text-gray-500">Há 35 min</span>
              </div>
              <div className="flex justify-between py-2 border-b">
                <span className="text-gray-900">Geração de Áudio ElevenLabs (#005)</span>
                <span className="text-gray-500">Há 40 min</span>
              </div>
              <div className="flex justify-between py-2">
                <span className="text-gray-900">Validação Ética (#011)</span>
                <span className="text-gray-500">Há 2 horas</span>
              </div>
            </div>
          </div>

        </div>
      </main>
    </div>
  )
}
