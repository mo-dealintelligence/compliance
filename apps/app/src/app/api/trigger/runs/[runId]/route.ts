import { auth } from '@/utils/auth';
import { runs } from '@trigger.dev/sdk';
import { headers } from 'next/headers';
import { NextResponse } from 'next/server';

/**
 * Run status for the @trigger.dev/react-hooks shim. Requires a session; a run
 * tagged with an organization id is only visible to members of that org.
 */
export async function GET(_request: Request, { params }: { params: Promise<{ runId: string }> }) {
  const { runId } = await params;
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  let run;
  try {
    run = await runs.retrieve(runId);
  } catch {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  const orgTags = run.tags.filter((t) => t.startsWith('org_') || t.startsWith('org:'));
  const activeOrg = session.session.activeOrganizationId;
  if (orgTags.length > 0 && !orgTags.some((t) => t === activeOrg || t === `org:${activeOrg}`)) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  return NextResponse.json({
    id: run.id,
    taskIdentifier: run.taskIdentifier,
    status: run.status,
    payload: run.payload,
    output: run.output,
    metadata: run.metadata,
    error: run.error ?? null,
    isCompleted: run.isCompleted,
    isSuccess: run.isSuccess,
    isFailed: run.isFailed,
    createdAt: run.createdAt,
    finishedAt: run.finishedAt,
  });
}
