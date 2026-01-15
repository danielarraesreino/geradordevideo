import { NextResponse } from 'next/server';
import { getAssets } from '@/lib/api-utils';

export async function GET() {
    try {
        const assets = getAssets();
        return NextResponse.json(assets);
    } catch (error) {
        return NextResponse.json({ error: 'Failed to fetch assets' }, { status: 500 });
    }
}
