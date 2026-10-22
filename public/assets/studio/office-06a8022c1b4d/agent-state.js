// Read-only presentation derived from task/run facts, never timers or invented AI activity.
export function getAgentState(agentId,officeId,snapshot){
 const projects=new Set(snapshot.projects.filter(p=>p.office_id===officeId).map(p=>p.id));
 const tasks=snapshot.tasks.filter(t=>t.agent_id===agentId&&projects.has(t.project_id));
 const active=tasks.find(t=>t.status==='running'&&snapshot.runs.some(r=>r.task_id===t.id&&r.status==='running'));
 if(active){const run=snapshot.runs.find(r=>r.task_id===active.id&&r.status==='running');return {phase:'working',label:run.provider==='demo-local'?'Al lavoro · DEMO locale':'Al lavoro',task:active,provider:run.provider};}
 const error=tasks.find(t=>t.status==='error');if(error)return {phase:'error',label:'Errore incarico',task:error};
 const review=tasks.find(t=>t.status==='review');if(review)return {phase:'review',label:'In revisione umana',task:review};
 const queue=tasks.find(t=>['queued','paused','blocked','running'].includes(t.status));if(queue)return {phase:'waiting',label:queue.status==='blocked'?'Bloccato':queue.status==='paused'?'In pausa':'In attesa',task:queue};
 const pending=tasks.find(t=>t.status==='todo');if(pending)return {phase:'waiting',label:['ai','video','external'].includes(pending.kind)?'In attesa · provider non collegato':'In attesa di avvio',task:pending};
 const done=tasks.filter(t=>t.status==='done').at(-1);if(done)return {phase:'done',label:'Incarico completato',task:done};
 return {phase:'idle',label:'Inattivo',task:null};
}
export function agentAssignments(agentIds,layout){
 const result=new Map();
 for(const zone of layout.zones)for(const id of zone.agents)if(agentIds.includes(id)&&!result.has(id))result.set(id,zone.id);
 for(const id of agentIds)if(!result.has(id))result.set(id,layout.zones[0].id);
 return result;
}
