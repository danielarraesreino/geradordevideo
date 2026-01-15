import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(request: NextRequest) {
    const { searchParams } = new URL(request.url);
    const name = searchParams.get('name');

    if (!name) {
        return NextResponse.json({ error: 'Image name is required' }, { status: 400 });
    }

    const PROJECT_ROOT = path.resolve(process.cwd(), '..');
    const imagesDir = path.join(PROJECT_ROOT, 'output', 'images_unsplash');
    const imagePath = path.join(imagesDir, name);

    if (!fs.existsSync(imagePath)) {
        return NextResponse.json({ error: 'Image not found' }, { status: 404 });
    }

    const imageBuffer = fs.readFileSync(imagePath);
    const ext = path.extname(name).toLowerCase();
    const contentTypeMap: Record<string, string> = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/white',
        '.webp': 'image/webp'
    };

    return new NextResponse(imageBuffer, {
        headers: {
            'Content-Type': contentTypeMap[ext] || 'application/octet-stream',
            'Cache-Control': 'public, max-age=31536000, immutable'
        }
    });
}
