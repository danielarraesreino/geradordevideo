import { NextRequest, NextResponse } from 'next/server';
import { getStoryById, saveStoryScript } from '@/lib/api-utils';

export async function GET(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    const { id } = await params;
    const story = getStoryById(id);

    if (!story) {
        return NextResponse.json({ error: 'Story not found' }, { status: 404 });
    }

    return NextResponse.json(story);
}

export async function POST(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    const { id } = await params;
    const { content } = await request.json();

    if (!content) {
        return NextResponse.json({ error: 'Content is required' }, { status: 400 });
    }

    const success = saveStoryScript(id, content);

    if (!success) {
        return NextResponse.json({ error: 'Failed to save story' }, { status: 500 });
    }

    return NextResponse.json({ success: true });
}
