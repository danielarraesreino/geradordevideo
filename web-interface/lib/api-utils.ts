import fs from 'fs';
import path from 'path';

// Helper to find the project root that contains 'data' and 'output'
function findProjectRoot() {
    const currentPath = process.cwd();
    // Check if we are in web-interface or the root
    if (fs.existsSync(path.join(currentPath, 'data')) && fs.existsSync(path.join(currentPath, 'output'))) {
        return currentPath;
    }
    const parentPath = path.resolve(currentPath, '..');
    if (fs.existsSync(path.join(parentPath, 'data')) && fs.existsSync(path.join(parentPath, 'output'))) {
        return parentPath;
    }
    // Fallback to current dir if not found (Vercel might have them in root if configured)
    return currentPath;
}

const PROJECT_ROOT = findProjectRoot();
const CSV_PATH = path.join(PROJECT_ROOT, 'data', 'historias_base.csv');
const OUTPUT_DIR = path.join(PROJECT_ROOT, 'output');

export interface Story {
    id: string;
    LOCAL_COMUM: string;
    NOME_FICTICIO: string;
    CONFLITO_PRINCIPAL: string;
    DICA_CAPACITACAO: string;
    tema_narrativo: string;
    eixo_canal: string;
    lei_relevante: string;
    gancho_estatistico: string;
    script?: string;
    slug?: string;
}

export function getAllStories(): Story[] {
    if (!fs.existsSync(CSV_PATH)) return [];

    const content = fs.readFileSync(CSV_PATH, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim() !== '');
    const headers = lines[0].split(',');

    return lines.slice(1).map(line => {
        const values = line.split(',');
        const story: any = {};
        headers.forEach((header, index) => {
            story[header] = values[index];
        });
        return story as Story;
    });
}

export function getStoryById(id: string): Story | null {
    const stories = getAllStories();
    const story = stories.find(s => s.id === id);
    if (!story) return null;

    // Try to find the markdown script
    const files = fs.readdirSync(OUTPUT_DIR);
    const scriptFile = files.find(f => f.startsWith(`historia_${id}_`) && f.endsWith('.md'));

    if (scriptFile) {
        const scriptPath = path.join(OUTPUT_DIR, scriptFile);
        story.script = fs.readFileSync(scriptPath, 'utf-8');
        story.slug = scriptFile.replace(`historia_${id}_`, '').replace('.md', '');
    }

    return story;
}

export function saveStoryScript(id: string, content: string): boolean {
    const stories = getAllStories();
    const story = stories.find(s => s.id === id);
    if (!story) return false;

    const files = fs.readdirSync(OUTPUT_DIR);
    let scriptFile = files.find(f => f.startsWith(`historia_${id}_`) && f.endsWith('.md'));

    if (!scriptFile) {
        // Create a default slug if doesn't exist
        const slug = story.NOME_FICTICIO.toLowerCase().replace(/\s+/g, '_');
        scriptFile = `historia_${id}_${slug}.md`;
    }

    const scriptPath = path.join(OUTPUT_DIR, scriptFile);
    fs.writeFileSync(scriptPath, content, 'utf-8');
    return true;
}

export function getAssets() {
    const imagesDir = path.join(OUTPUT_DIR, 'images_unsplash');
    if (!fs.existsSync(imagesDir)) return [];

    return fs.readdirSync(imagesDir)
        .filter(f => /\.(jpg|jpeg|png|webp)$/i.test(f))
        .map(f => ({
            name: f,
            url: `/api/proxy-image?name=${f}` // We'll need a proxy for external images outside public/
        }));
}
