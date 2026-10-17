/* Dependency-free, read-only public evidence viewer. No data mutations or persistent storage. */
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const escape = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const label = (value) => String(value ?? '').replaceAll('_', ' ');
  const badge = (value, extra = '') => `<span class="badge ${escape(extra || value)}">${escape(label(value))}</span>`;
  const kindName = (kind) => ({public_case:'Primary-source case',public_snapshot:'Editorial source review'}[kind] || 'Public record');
  const claimStatusName = (status) => status === 'supported' ? 'Supported by cited source' : label(status);
  const date = (value) => {
    if (!value) return 'Date not supplied';
    if (/^\d{4}-\d{2}-\d{2}$/.test(value)) return new Date(`${value}T00:00:00Z`).toLocaleDateString('en-GB', {day:'numeric',month:'short',year:'numeric',timeZone:'UTC'});
    const parsed = new Date(value);
    return Number.isNaN(parsed.valueOf()) ? value : `${parsed.toLocaleDateString('en-GB', {day:'numeric',month:'short',year:'numeric',timeZone:'UTC'})} · ${parsed.toLocaleTimeString('en-GB', {hour:'2-digit',minute:'2-digit',timeZone:'UTC'})} UTC`;
  };
  const safeUrl = (value) => {
    if (typeof value !== 'string') return '#provenance';
    if (/^https:\/\//i.test(value)) {
      try { const parsed = new URL(value); return parsed.protocol === 'https:' && !parsed.username && !parsed.password ? parsed.href : '#provenance'; } catch { return '#provenance'; }
    }
    return /^(\/(?!\/)[a-zA-Z0-9/_\-.]+|\.\/data\/[a-zA-Z0-9_.-]+|#[a-zA-Z0-9_-]+)$/.test(value) ? value : '#provenance';
  };
  let bundle = null;
  let selected = null;
  let missingCase = false;

  function readLocation() {
    const params = new URLSearchParams(location.search);
    $('case-search').value = params.get('q') || '';
    $('case-kind').value = ['public_case','public_snapshot'].includes(params.get('kind')) ? params.get('kind') : 'all';
    $('case-status').value = ['documented','developing','under_review'].includes(params.get('status')) ? params.get('status') : 'all';
    $('relationship-filter').value = ['supports','contradicts','ambiguous'].includes(params.get('relationship')) ? params.get('relationship') : 'all';
    const requested = params.get('case');
    missingCase = Boolean(requested && !bundle.cases.some((item) => item.id === requested));
    selected = bundle.cases.find((item) => item.id === requested) || bundle.cases[0];
  }

  function caseUrl(id, hash = 'case-workspace') {
    const params = new URLSearchParams();
    params.set('case', id);
    if ($('case-search').value.trim()) params.set('q', $('case-search').value.trim());
    if ($('case-kind').value !== 'all') params.set('kind', $('case-kind').value);
    if ($('case-status').value !== 'all') params.set('status', $('case-status').value);
    if ($('relationship-filter').value !== 'all') params.set('relationship', $('relationship-filter').value);
    return `${location.pathname}?${params.toString()}${hash ? `#${hash}` : ''}`;
  }

  function syncLocation(push = false, hash = location.hash.slice(1)) {
    const href = caseUrl(selected?.id || bundle.cases[0].id, hash);
    if (`${location.pathname}${location.search}${location.hash}` !== href) history[push ? 'pushState' : 'replaceState'](null, '', href);
  }

  function sourceLink(source, text = source.title) {
    return `<a class="source-inline" href="${escape(safeUrl(source.url))}">${escape(text)}</a>`;
  }

  function sourceRefs(ids) {
    return (ids || []).map((id) => selected.sources.find((source) => source.id === id)).filter(Boolean).map((source) => `<a href="#source-${escape(source.id)}">${escape(source.publisher)}</a>`).join(' · ');
  }

  function retrievalReceipt(receipt, title = 'Access check: original source') {
    const receiptLabel = receipt?.status === 'retrieved' ? 'Retrieved' : receipt?.status === 'unavailable' ? 'Could not retrieve' : 'No access check recorded';
    return `<section class="source-check" aria-label="${escape(title)}"><h4>${escape(title)}</h4>${badge(receiptLabel, receipt?.status || 'unknown')}<p>${receipt?.retrieved_at ? `Attempted ${escape(date(receipt.retrieved_at))}` : 'No retrieval time recorded.'}${receipt?.method ? `<br>Method: ${escape(label(receipt.method))}` : ''}${receipt?.http_status != null ? `<br>HTTP status: ${escape(receipt.http_status)}` : ''}${receipt?.content_type ? `<br>Content type: ${escape(receipt.content_type)}` : ''}${receipt?.bytes != null ? `<br>Response bytes: ${escape(receipt.bytes)}` : ''}</p>${receipt?.final_url ? `<p><a href="${escape(safeUrl(receipt.final_url))}">Open response URL ↗</a></p>` : ''}${receipt?.body_sha256 ? `<p class="rights">Response fingerprint; content not archived<br>SHA-256: <code>${escape(receipt.body_sha256)}</code></p>` : '<p class="rights">No response fingerprint recorded.</p>'}${receipt?.error ? `<p>${escape(receipt.error)}</p>` : ''}<p class="rights">This access check does not verify the source’s claims.</p></section>`;
  }

  function publicCopyLinks(source) {
    const reviewedUrl = source.verification?.reviewed_url;
    const reviewedLink = reviewedUrl && reviewedUrl !== source.url ? `<a href="${escape(safeUrl(reviewedUrl))}">Read the public copy checked ↗</a>` : '';
    const alternateLink = source.alternate_url && source.alternate_url !== source.url && source.alternate_url !== reviewedUrl ? `<a href="${escape(safeUrl(source.alternate_url))}">Read the republished article ↗</a>` : '';
    return reviewedLink || alternateLink ? `<div class="public-copy-links">${reviewedLink}${alternateLink}</div>` : '';
  }

  function sourceChecks(source) {
    const review = source.verification;
    const reviewLabel = review?.status === 'content_reviewed' ? 'Content reviewed' : review?.status === 'not_accessible' ? 'Content not accessible' : 'Content review unknown';
    const reviewBlock = `<section class="source-check" aria-label="Source-content check"><h4>Source-content check</h4>${badge(reviewLabel, review?.status || 'unknown')}<p>${review?.checked_at ? `Checked ${escape(date(review.checked_at))}` : 'No source-check date recorded.'}${review?.method ? `<br>Method: ${escape(label(review.method))}` : ''}</p>${review?.locator ? `<p><strong>Where to find it</strong><br>${escape(review.locator)}</p>` : ''}<p>${escape(review?.note || 'No content check is recorded for this source.')}</p>${review?.access_note ? `<p><strong>Access note</strong><br>${escape(review.access_note)}</p>` : ''}</section>`;
    return `<div class="source-checks">${reviewBlock}${retrievalReceipt(source.retrieval)}${source.alternate_retrieval ? retrievalReceipt(source.alternate_retrieval, 'Access check: public copy') : ''}</div>`;
  }

  function renderCheckSummary() {
    const dates = bundle.cases.flatMap((item) => item.sources.flatMap((source) => [source.verification?.checked_at, source.retrieval?.retrieved_at, source.alternate_retrieval?.retrieved_at])).filter((value) => value && !Number.isNaN(new Date(value).valueOf())).sort((a, b) => new Date(a) - new Date(b));
    $('source-check-summary').textContent = dates.length ? `Latest source check: ${date(dates[dates.length - 1])}. Dates and access results appear with each source.` : 'No source-check dates are recorded.';
  }

  function renderRegistry() {
    const query = $('case-search').value.trim().toLocaleLowerCase();
    const words = query.split(/\s+/).filter(Boolean);
    const matches = bundle.cases.filter((item) => {
      const haystack = [item.title,item.summary,item.status,...item.tags,...(item.comparisons || []).flatMap((comparison) => [comparison.metric,comparison.assessment,comparison.note,comparison.followup?.summary,comparison.target?.period,comparison.actual?.period]),...item.claims.flatMap((claim) => [claim.text,claim.kind,claim.status,claim.caveat,claim.locator]),...item.sources.flatMap((source) => [source.title,source.publisher,source.notes,source.verification?.note]),...(item.open_questions || []).flatMap((question) => [question.question,question.why_it_matters,question.needed_evidence])].join(' ').toLocaleLowerCase();
      return words.every((word) => haystack.includes(word)) && ($('case-kind').value === 'all' || item.kind === $('case-kind').value) && ($('case-status').value === 'all' || item.status === $('case-status').value);
    });
    if (matches.length && !matches.some((item) => item.id === selected?.id)) selected = matches[0];
    $('results-count').textContent = `${matches.length} of ${bundle.cases.length} cases${query ? ` matching “${$('case-search').value.trim()}”` : ''}.${missingCase ? ' Requested case not found; showing available cases.' : ''}`;
    $('case-list').innerHTML = matches.length ? matches.map((item) => `<article class="case-card ${item.id === selected.id ? 'active' : ''}"><div class="card-top">${badge(kindName(item.kind), item.kind)}${badge(item.status)}</div><h3><a href="${escape(caseUrl(item.id))}" data-case="${escape(item.id)}"${item.id === selected.id ? ' aria-current="true"' : ''}>${escape(item.title)}</a></h3><p>${escape(item.summary)}</p><div class="card-meta"><span>${item.claims.length} claims · ${item.sources.length} sources · ${(item.open_questions || []).length} open questions</span><a href="${escape(caseUrl(item.id))}" data-case="${escape(item.id)}">Read case <span aria-hidden="true">↗</span><span class="sr-only">: ${escape(item.title)}</span></a></div></article>`).join('') : '<div class="empty-state"><h3>No cases match these filters.</h3><p>Try a broader search or use “Clear filters” to return to all cases.</p></div>';
    $('case-workspace').hidden = matches.length === 0;
    if (matches.length) renderCase();
  }

  function comparisonValue(entry, heading) {
    if (!entry) return '';
    const value = entry.value == null ? 'Not reported' : typeof entry.value === 'number' ? entry.value.toLocaleString('en-GB') : String(entry.value);
    const source = selected.sources.find((item) => item.id === entry.source_id);
    return `<section class="comparison-value"><h4>${escape(heading)}</h4><p class="comparison-number">${escape(value)}${entry.value != null && entry.unit ? ` <span>${escape(entry.unit)}</span>` : ''}</p>${entry.period ? `<p><strong>Period</strong><br>${escape(entry.period)}</p>` : ''}${source ? `<p><a href="#source-${escape(source.id)}">${escape(source.publisher)}: ${escape(source.title)}</a></p>` : ''}${entry.locator ? `<p><strong>Where to find it</strong><br>${escape(entry.locator)}</p>` : ''}</section>`;
  }

  function comparisonFollowup(followup) {
    if (!followup || typeof followup.summary !== 'string') return '';
    const sources = (Array.isArray(followup.source_ids) ? followup.source_ids : []).map((id) => selected.sources.find((source) => source.id === id)).filter(Boolean);
    return `<p><strong>Follow-up</strong><br>${escape(followup.summary)}</p>${sources.length ? `<p>Sources: ${sources.map((source) => `<a href="#source-${escape(source.id)}">${escape(source.title)}</a>`).join(' · ')}</p>` : ''}`;
  }

  function renderComparisons() {
    const comparisons = selected.comparisons || [];
    $('comparisons').hidden = comparisons.length === 0;
    $('comparison-nav').hidden = comparisons.length === 0;
    $('comparison-list').innerHTML = comparisons.map((comparison) => `<article class="comparison-card" id="comparison-${escape(comparison.id)}"><h3>${escape(comparison.metric)}</h3><div class="comparison-values">${comparisonValue(comparison.target, 'Plan')}${comparisonValue(comparison.actual, 'UNHCR reported')}</div>${comparison.assessment ? `<p class="comparison-assessment"><strong>Assessment</strong><br>${escape(comparison.assessment)}</p>` : ''}${comparison.note ? `<p>${escape(comparison.note)}</p>` : ''}${comparisonFollowup(comparison.followup)}${comparison.calculation ? `<p class="comparison-calculation"><strong>Calculation</strong><br>${escape(comparison.calculation)}</p>` : ''}</article>`).join('');
  }

  function renderCorrections() {
    const changes = selected.corrections || [];
    $('correction-list').innerHTML = changes.length ? changes.map((correction, index) => {
      const kind = correction.kind || 'correction';
      const before = correction.before_snapshot || {};
      const after = correction.after_snapshot || {};
      const recorded = correction.recorded_at || correction.corrected_at || correction.published_at;
      return `<details class="correction" id="correction-${escape(correction.id)}"${index === 0 ? ' open' : ''}><summary>${badge(kind)}<strong>${escape(correction.claim_id || correction.id)}</strong>${recorded ? `<time class="change-time" datetime="${escape(recorded)}">${escape(date(recorded))}</time>` : ''}</summary><div class="change-body"><p>${escape(correction.cause)}</p><p><a href="#revision-${escape(correction.from_revision_id)}">${escape(correction.from_revision_id)}</a> → <a href="#revision-${escape(correction.to_revision_id)}">${escape(correction.to_revision_id)}</a></p>${correction.before == null && !before.text ? '<p class="new-claim">New claim; no earlier wording.</p>' : `<blockquote class="before"><span class="change-label">Earlier wording</span>${escape(correction.before ?? before.text)}${correction.before_status || before.status ? `<p>Status: ${escape(claimStatusName(correction.before_status || before.status))}</p>` : ''}${before.caveat ? `<p><strong>Limits</strong><br>${escape(before.caveat)}</p>` : ''}${before.locator ? `<p>${escape(before.locator)}</p>` : ''}${before.source_ids?.length ? `<p>Sources: ${sourceRefs(before.source_ids)}</p>` : ''}</blockquote>`}<blockquote class="after"><span class="change-label">${kind === 'correction' ? 'Corrected wording' : 'Updated wording'}</span>${escape(correction.after ?? after.text)}${correction.after_status || after.status ? `<p>Status: ${escape(claimStatusName(correction.after_status || after.status))}</p>` : ''}${after.caveat ? `<p><strong>Limits</strong><br>${escape(after.caveat)}</p>` : ''}${after.locator ? `<p>${escape(after.locator)}</p>` : ''}${after.source_ids?.length ? `<p>Sources: ${sourceRefs(after.source_ids)}</p>` : ''}</blockquote>${correction.source_ids?.length ? `<p>Sources for this change: ${sourceRefs(correction.source_ids)}</p>` : ''}${correction.claim_id ? `<a href="#claim-${escape(correction.claim_id)}">Read current claim ↑</a>` : ''}</div></details>`;
    }).join('') : '<p class="muted">No updates or corrections are recorded for this case.</p>';
  }

  function renderRevisions() {
    $('revision-list').innerHTML = (selected.revisions || []).length ? selected.revisions.map((revision, index) => {
      const title = revision.historical_import ? 'Previously published version' : index === selected.revisions.length - 1 ? 'Current revision' : 'Earlier revision';
      const stamp = revision.historical_import ? 'Verified by' : 'Revision date';
      const commitUrl = /^[a-f0-9]{7,40}$/.test(revision.source_commit || '') && /^[a-zA-Z0-9/_\-.]+$/.test(revision.source_path || '') ? `https://github.com/Parallax-Web-Services/spacezh/blob/${revision.source_commit}/${revision.source_path}` : null;
      return `<details class="revision" id="revision-${escape(revision.id)}"><summary><strong>${escape(title)}</strong> · ${escape(revision.id)}<span class="revision-meta">${stamp}: ${escape(date(revision.published_at))}</span></summary><div class="revision-body"><p>${escape(revision.change_note)}</p>${revision.import_note ? `<p>${escape(revision.import_note)}</p>` : ''}${commitUrl ? `<p><a href="${escape(commitUrl)}">Read the source at ${escape(revision.source_commit.slice(0, 7))} ↗</a></p>` : ''}<p>Previous revision: ${escape(revision.parent_revision_id || 'None recorded')}<br>Reviews: ${(revision.review_ids || []).length ? revision.review_ids.map((id) => `<a href="#review-${escape(id)}">${escape(id)}</a>`).join(', ') : 'None recorded'}</p>${revision.snapshot_sha256 ? `<p class="fingerprint">Snapshot SHA-256: <code>${escape(revision.snapshot_sha256)}</code></p>` : ''}<ul>${(revision.claim_snapshots || []).map((snapshot) => `<li><strong>${escape(snapshot.claim_id)} · ${escape(claimStatusName(snapshot.status))}</strong><br>${escape(snapshot.text)}${snapshot.caveat ? `<p><strong>Limits</strong><br>${escape(snapshot.caveat)}</p>` : ''}${snapshot.locator ? `<p>${escape(snapshot.locator)}</p>` : ''}${snapshot.source_ids?.length ? `<p>Sources: ${sourceRefs(snapshot.source_ids)}</p>` : ''}</li>`).join('')}</ul></div></details>`;
    }).join('') : '<p class="muted">No revision history is recorded for this case.</p>';
  }

  function renderReviews() {
    $('review-list').innerHTML = (selected.reviews || []).length ? selected.reviews.map((review) => {
      const human = review.kind === 'human' && review.reviewer_type === 'human';
      return `<article class="review" id="review-${escape(review.id)}">${badge(human ? 'Human review' : 'AI-assisted review', human ? 'human_review' : 'ai_assisted')}<h4>${escape(review.reviewer)}</h4>${review.reviewed_at ? `<p>Checked ${escape(date(review.reviewed_at))}</p>` : ''}<p><strong>Scope</strong><br>${escape(review.scope || 'Not recorded')}</p>${review.method ? `<p><strong>Method</strong><br>${escape(review.method)}</p>` : ''}<p><strong>Result: ${escape(label(review.decision))}</strong><br>${escape(review.rationale)}</p>${!human ? '<p class="review-boundary">This AI-assisted check does not record human editorial approval.</p>' : ''}${review.revision_id ? `<p>Revision: <a href="#revision-${escape(review.revision_id)}">${escape(review.revision_id)}</a></p>` : ''}<p>Attribution and conflicts: ${escape(review.conflicts)}</p>${review.snapshot_sha256 ? `<p class="fingerprint">Claim snapshot SHA-256: <code>${escape(review.snapshot_sha256)}</code></p>` : ''}</article>`;
    }).join('') : '<p class="muted">No case-level review or human editorial approval is recorded. Source checks appear with each source.</p>';
  }

  function renderCase() {
    $('case-overview').innerHTML = `<div class="overview-label">${badge(kindName(selected.kind), selected.kind)}${badge(selected.status)}<span class="case-id">${escape(selected.id)}</span></div><h2 id="case-title" tabindex="-1">${escape(selected.title)}</h2><p class="case-summary">${escape(selected.summary)}</p><p class="case-boundary">${escape(selected.boundary_note)}</p><div class="tag-list">${selected.tags.map((tag) => `<span>${escape(tag)}</span>`).join('')}</div><div class="case-actions"><button type="button" id="copy-case-link">Copy case link</button><a href="./data/cases.json" download="spacezh-relay-public-cases.json">Download case data (JSON)</a><a href="./data/retrievals.json" download="spacezh-relay-retrievals.json">Download access log (JSON)</a>${selected.kind === 'public_snapshot' ? `<a href="${escape(safeUrl(selected.provenance.url))}">Read original public brief ↗</a>` : ''}<span class="permalink-feedback" id="copy-feedback" role="status" aria-live="polite"></span></div>`;
    $('claim-count').textContent = `(${selected.claims.length})`;
    renderComparisons();
    $('claim-list').innerHTML = selected.claims.map((claim) => {
      const links = selected.evidence_links.filter((link) => link.claim_id === claim.id);
      return `<details class="claim" id="claim-${escape(claim.id)}"><summary><div><span class="claim-label">${escape(claim.kind)}</span>${badge(claimStatusName(claim.status), claim.status)}</div><span class="claim-text">${escape(claim.text)}</span></summary><div class="claim-body"><p><strong>Limits</strong><br>${escape(claim.caveat)}</p>${claim.locator ? `<p><strong>Where to find it</strong><br>${escape(claim.locator)}</p>` : ''}<p><strong>Supporting and conflicting sources</strong><br>Each link applies to the wording of this claim.</p><ul>${links.map((link) => `<li><span class="relationship-line">${escape(label(link.relationship))} · ${sourceRefs([link.source_id])}</span><br>${escape(link.rationale)}</li>`).join('')}</ul><div class="claim-links"><a href="${escape(caseUrl(selected.id, `claim-${claim.id}`))}" data-claim-link="claim-${escape(claim.id)}">Permanent claim link</a><a href="#evidence">See evidence links ↓</a></div></div></details>`;
    }).join('');
    renderLedger();
    $('question-list').innerHTML = (selected.open_questions || []).length ? selected.open_questions.map((question, index) => `<article class="question-card"><span class="source-meta">OPEN QUESTION ${index + 1}</span><h3>${escape(question.question)}</h3><p><strong>Why it matters</strong><br>${escape(question.why_it_matters)}</p><p><strong>Evidence needed</strong><br>${escape(question.needed_evidence)}</p>${question.source_ids?.length ? `<p>Related sources: ${sourceRefs(question.source_ids)}</p>` : ''}</article>`).join('') : '<p class="muted">No open questions are recorded for this case.</p>';
    $('timeline-list').innerHTML = (selected.timeline || []).length ? selected.timeline.map((event) => `<li><time class="time" datetime="${escape(event.date)}">${escape(date(event.date))}</time><strong>${escape(event.label)}</strong><p>${escape(event.detail)}</p>${event.source_ids?.length ? `<p>${sourceRefs(event.source_ids)}</p>` : ''}${event.revision_id ? `<p><a href="#revision-${escape(event.revision_id)}">See revision ${escape(event.revision_id)} ↓</a></p>` : ''}</li>`).join('') : '<li><p>No timeline has been recorded for this case.</p></li>';
    renderCorrections();
    renderRevisions();
    $('provenance-summary').innerHTML = `<p>${escape(selected.provenance.note)}</p><p>${escape(selected.publication_note)}</p><p><a href="${escape(safeUrl(selected.provenance.url))}">${escape(selected.provenance.label)} ↗</a></p>${selected.source_independence_notes.length ? `<ul>${selected.source_independence_notes.map((note) => `<li>${escape(note)}</li>`).join('')}</ul>` : ''}`;
    $('source-list').innerHTML = selected.sources.map((source) => {
      return `<article class="source-card" id="source-${escape(source.id)}"><span class="source-meta">${escape(source.publisher)} / ${escape(date(source.published_date))}</span><h3>${escape(source.title)}</h3><p class="source-meta">${escape(label(source.source_type))}${source.byline ? ` · ${escape(source.byline)}` : ''}</p><p>${escape(source.notes)}</p>${sourceLink(source, 'Read source ↗')}${publicCopyLinks(source)}<p class="rights">${escape(source.rights)}</p>${sourceChecks(source)}</article>`;
    }).join('');
    renderReviews();
    $('copy-case-link').addEventListener('click', copyCaseLink);
    revealHash(false);
  }

  function renderLedger() {
    const value = $('relationship-filter').value;
    const links = selected.evidence_links.filter((link) => value === 'all' || link.relationship === value);
    $('evidence-body').innerHTML = links.map((link) => {
      const claim = selected.claims.find((item) => item.id === link.claim_id);
      const source = selected.sources.find((item) => item.id === link.source_id);
      return `<tr><td><a href="#claim-${escape(claim.id)}">${escape(claim.id)}</a><p>${escape(claim.kind)}</p></td><td>${badge(link.relationship)}</td><td>${sourceLink(source)}<p>${escape(link.rationale)}</p><p><a href="#source-${escape(source.id)}">Source details ↓</a></p></td></tr>`;
    }).join('');
    $('ledger-count').textContent = `${links.length} of ${selected.evidence_links.length} relationships`;
    $('ledger-empty').hidden = links.length > 0;
  }

  function revealHash(scroll = true) {
    const id = location.hash.slice(1);
    if (!id) return;
    const target = $(id);
    if (!target) return;
    if (target.tagName === 'DETAILS') target.open = true;
    if (scroll) target.scrollIntoView({block:'start', behavior:'instant'});
  }

  async function copyCaseLink() {
    const link = new URL(caseUrl(selected.id), location.href).href;
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(link);
      $('copy-feedback').textContent = 'Case link copied.';
    } catch {
      syncLocation(false, 'case-workspace');
      $('copy-feedback').textContent = 'Copy the case link from your address bar.';
    }
  }

  async function load() {
    $('load-error').hidden = true;
    $('results-count').textContent = 'Loading cases…';
    $('retry-load').disabled = true;
    try {
      const response = await fetch('./data/cases.json', {cache:'no-store'});
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      if (data.schema_version !== 'spacezh.relay.prototype.v1' || data.prototype !== true || data.confidential_intake !== false || data.trusted_operational_feed !== false || !Array.isArray(data.cases) || !data.cases.length || data.cases.some((item) => !['public_case','public_snapshot'].includes(item.kind) || (item.reviews || []).some((review) => review.kind === 'simulated'))) throw new Error('Invalid public evidence bundle');
      bundle = data;
      renderCheckSummary();
      readLocation();
      renderRegistry();
      revealHash();
    } catch {
      $('case-list').innerHTML = '';
      $('case-workspace').hidden = true;
      $('results-count').textContent = 'Case data unavailable.';
      $('load-error').hidden = false;
    } finally {
      $('retry-load').disabled = false;
    }
  }

  $('case-filters').addEventListener('submit', (event) => event.preventDefault());
  $('case-search').addEventListener('input', () => { if (!bundle) return; missingCase = false; renderRegistry(); syncLocation(); });
  for (const id of ['case-kind','case-status']) $(id).addEventListener('change', () => { if (!bundle) return; missingCase = false; renderRegistry(); syncLocation(); });
  $('case-filters').addEventListener('reset', (event) => {
    event.preventDefault();
    $('case-search').value = '';
    $('case-kind').value = 'all';
    $('case-status').value = 'all';
    $('relationship-filter').value = 'all';
    if (!bundle) return;
    missingCase = false;
    renderRegistry();
    syncLocation();
  });
  $('case-list').addEventListener('click', (event) => {
    const anchor = event.target.closest('a[data-case]');
    if (!anchor || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    selected = bundle.cases.find((item) => item.id === anchor.dataset.case);
    missingCase = false;
    syncLocation(true, 'case-workspace');
    renderRegistry();
    $('case-title').focus({preventScroll:true});
    $('case-workspace').scrollIntoView({block:'start',behavior:'instant'});
  });
  $('relationship-filter').addEventListener('change', () => { if (!bundle || !selected) return; renderLedger(); syncLocation(); });
  $('retry-load').addEventListener('click', load);
  window.addEventListener('hashchange', () => revealHash());
  window.addEventListener('popstate', () => { if (!bundle) return; readLocation(); renderRegistry(); revealHash(); });
  load();
})();
