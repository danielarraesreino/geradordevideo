import { NextResponse } from 'next/server';
import { getAllStories } from '@/lib/api-utils';

export async function GET() {
    try {
        const stories = getAllStories();
        return NextResponse.json(stories);
    } catch (error) {
        return NextResponse.json({ error: 'Failed to fetch stories' }, { status: 500 });
    }
}
