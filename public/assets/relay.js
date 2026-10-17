/* Dependency-free, read-only public evidence viewer. No data mutations or persistent storage. */
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const escape = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const label = (value) => String(value ?? '').replaceAll('_', ' ');
  const badge = (value, extra = '') => `<span class="badge ${escape(extra || value)}">${escape(label(value))}</span>`;
  const kindName = (kind) => ({public_case:'Primary-source case',public_snapshot:'Editorial source review'}[kind] || 'Public record');
  const claimStatusName = (status) => status === 'supported' ? 'Source support recorded' : label(status);
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

  function retrievalReceipt(receipt, title = 'Original-source retrieval receipt') {
    const receiptLabel = receipt?.status === 'retrieved' ? 'Response retrieved' : receipt?.status === 'unavailable' ? 'Retrieval unavailable' : 'No retrieval recorded';
    return `<section class="source-check" aria-label="${escape(title)}"><h4>${escape(title)}</h4>${badge(receiptLabel, receipt?.status || 'unknown')}<p>${receipt?.retrieved_at ? `Attempted ${escape(date(receipt.retrieved_at))}` : 'No retrieval time recorded.'}${receipt?.method ? `<br>Method: ${escape(label(receipt.method))}` : ''}${receipt?.http_status != null ? `<br>HTTP status: ${escape(receipt.http_status)}` : ''}${receipt?.content_type ? `<br>Content type: ${escape(receipt.content_type)}` : ''}${receipt?.bytes != null ? `<br>Response bytes: ${escape(receipt.bytes)}` : ''}</p>${receipt?.final_url ? `<p><a href="${escape(safeUrl(receipt.final_url))}">Open recorded response URL ↗</a></p>` : ''}${receipt?.body_sha256 ? `<p class="rights">Retrieved response bytes; body not archived<br>SHA-256: <code>${escape(receipt.body_sha256)}</code></p>` : '<p class="rights">No response fingerprint recorded.</p>'}${receipt?.error ? `<p>${escape(receipt.error)}</p>` : ''}<p class="rights">This receipt records access and response bytes. It is not verification of the source’s claims.</p></section>`;
  }

  function publicCopyLinks(source) {
    const reviewedUrl = source.verification?.reviewed_url;
    const reviewedLink = reviewedUrl && reviewedUrl !== source.url ? `<a href="${escape(safeUrl(reviewedUrl))}">Read reviewed public copy ↗</a>` : '';
    const alternateLink = source.alternate_url && source.alternate_url !== source.url && source.alternate_url !== reviewedUrl ? `<a href="${escape(safeUrl(source.alternate_url))}">Read public syndication / republication ↗</a>` : '';
    return reviewedLink || alternateLink ? `<div class="public-copy-links">${reviewedLink}${alternateLink}</div>` : '';
  }

  function sourceChecks(source) {
    const review = source.verification;
    const reviewLabel = review?.status === 'content_reviewed' ? 'Content reviewed' : review?.status === 'not_accessible' ? 'Content not accessible' : 'Content review unknown';
    const reviewBlock = `<section class="source-check" aria-label="Source-content review"><h4>Source-content review</h4>${badge(reviewLabel, review?.status || 'unknown')}<p>${review?.checked_at ? `Checked ${escape(date(review.checked_at))}` : 'No content-review date recorded.'}${review?.method ? `<br>Method: ${escape(label(review.method))}` : ''}</p>${review?.locator ? `<p><strong>Locator</strong><br>${escape(review.locator)}</p>` : ''}<p>${escape(review?.note || 'The source content has not been recorded as reviewed. Access success alone does not resolve this unknown.')}</p>${review?.access_note ? `<p><strong>Access note</strong><br>${escape(review.access_note)}</p>` : ''}</section>`;
    return `<div class="source-checks">${reviewBlock}${retrievalReceipt(source.retrieval)}${source.alternate_retrieval ? retrievalReceipt(source.alternate_retrieval, 'Public-copy retrieval receipt') : ''}</div>`;
  }

  function renderCheckSummary() {
    const dates = bundle.cases.flatMap((item) => item.sources.flatMap((source) => [source.verification?.checked_at, source.retrieval?.retrieved_at, source.alternate_retrieval?.retrieved_at])).filter((value) => value && !Number.isNaN(new Date(value).valueOf())).sort((a, b) => new Date(a) - new Date(b));
    $('source-check-summary').textContent = dates.length ? `Latest recorded source check: ${date(dates[dates.length - 1])}. Review status and access limits appear with each source.` : 'No source-check dates recorded. Review status remains unknown until a check is recorded.';
  }

  function renderRegistry() {
    const query = $('case-search').value.trim().toLocaleLowerCase();
    const words = query.split(/\s+/).filter(Boolean);
    const matches = bundle.cases.filter((item) => {
      const haystack = [item.title,item.summary,item.status,...item.tags,...item.claims.flatMap((claim) => [claim.text,claim.kind,claim.status,claim.caveat,claim.locator]),...item.sources.flatMap((source) => [source.title,source.publisher,source.notes,source.verification?.note]),...(item.open_questions || []).flatMap((question) => [question.question,question.why_it_matters,question.needed_evidence])].join(' ').toLocaleLowerCase();
      return words.every((word) => haystack.includes(word)) && ($('case-kind').value === 'all' || item.kind === $('case-kind').value) && ($('case-status').value === 'all' || item.status === $('case-status').value);
    });
    if (matches.length && !matches.some((item) => item.id === selected?.id)) selected = matches[0];
    $('results-count').textContent = `${matches.length} of ${bundle.cases.length} records${query ? ` matching “${$('case-search').value.trim()}”` : ''}.${missingCase ? ' Requested case not found; showing available records.' : ''}`;
    $('case-list').innerHTML = matches.length ? matches.map((item) => `<article class="case-card ${item.id === selected.id ? 'active' : ''}"><div class="card-top">${badge(kindName(item.kind), item.kind)}${badge(item.status)}</div><h3><a href="${escape(caseUrl(item.id))}" data-case="${escape(item.id)}"${item.id === selected.id ? ' aria-current="true"' : ''}>${escape(item.title)}</a></h3><p>${escape(item.summary)}</p><div class="card-meta"><span>${item.claims.length} claims · ${item.sources.length} sources · ${(item.open_questions || []).length} open questions</span><a href="${escape(caseUrl(item.id))}" data-case="${escape(item.id)}">Open record <span aria-hidden="true">↗</span><span class="sr-only">: ${escape(item.title)}</span></a></div></article>`).join('') : '<div class="empty-state"><h3>No cases match these filters.</h3><p>Try a broader search or use “Clear filters” to return to all records.</p></div>';
    $('case-workspace').hidden = matches.length === 0;
    if (matches.length) renderCase();
  }

  function renderCase() {
    $('case-overview').innerHTML = `<div class="overview-label">${badge(kindName(selected.kind), selected.kind)}${badge(selected.status)}<span class="case-id">${escape(selected.id)}</span></div><h2 id="case-title" tabindex="-1">${escape(selected.title)}</h2><p class="case-summary">${escape(selected.summary)}</p><p class="case-boundary">${escape(selected.boundary_note)}</p><div class="tag-list">${selected.tags.map((tag) => `<span>${escape(tag)}</span>`).join('')}</div><div class="case-actions"><button type="button" id="copy-case-link">Copy case link</button><a href="./data/cases.json" download="spacezh-relay-public-cases.json">Download public evidence (JSON)</a><a href="./data/retrievals.json" download="spacezh-relay-retrievals.json">Download retrieval log (JSON)</a>${selected.kind === 'public_snapshot' ? `<a href="${escape(safeUrl(selected.provenance.url))}">Read original public brief ↗</a>` : ''}<span class="permalink-feedback" id="copy-feedback" role="status" aria-live="polite"></span></div>`;
    $('claim-count').textContent = `(${selected.claims.length})`;
    $('claim-list').innerHTML = selected.claims.map((claim) => {
      const links = selected.evidence_links.filter((link) => link.claim_id === claim.id);
      return `<details class="claim" id="claim-${escape(claim.id)}"><summary><div><span class="claim-label">${escape(claim.kind)}</span>${badge(claimStatusName(claim.status), claim.status)}</div><span class="claim-text">${escape(claim.text)}</span></summary><div class="claim-body"><p><strong>Limits & uncertainty</strong><br>${escape(claim.caveat)}</p>${claim.locator ? `<p><strong>Document locator</strong><br>${escape(claim.locator)}</p>` : ''}<p><strong>Evidence relationships</strong><br>Source support records a relationship to this wording; it does not establish every underlying fact.</p><ul>${links.map((link) => `<li><span class="relationship-line">${escape(label(link.relationship))} · ${sourceRefs([link.source_id])}</span><br>${escape(link.rationale)}</li>`).join('')}</ul><div class="claim-links"><a href="${escape(caseUrl(selected.id, `claim-${claim.id}`))}" data-claim-link="claim-${escape(claim.id)}">Permanent claim link</a><a href="#evidence">Inspect evidence ledger ↓</a></div></div></details>`;
    }).join('');
    renderLedger();
    $('question-list').innerHTML = (selected.open_questions || []).length ? selected.open_questions.map((question, index) => `<article class="question-card"><span class="source-meta">OPEN QUESTION ${index + 1}</span><h3>${escape(question.question)}</h3><p><strong>Why it matters</strong><br>${escape(question.why_it_matters)}</p><p><strong>Evidence needed</strong><br>${escape(question.needed_evidence)}</p>${question.source_ids?.length ? `<p>Related source records: ${sourceRefs(question.source_ids)}</p>` : ''}</article>`).join('') : '<p class="muted">No verification questions have been recorded for this case. That does not establish that the case is complete.</p>';
    $('timeline-list').innerHTML = (selected.timeline || []).length ? selected.timeline.map((event) => `<li><time class="time" datetime="${escape(event.date)}">${escape(date(event.date))}</time><strong>${escape(event.label)}</strong><p>${escape(event.detail)}</p>${event.source_ids?.length ? `<p>${sourceRefs(event.source_ids)}</p>` : ''}${event.revision_id ? `<p><a href="#revision-${escape(event.revision_id)}">Inspect ${escape(event.revision_id)} ↓</a></p>` : ''}</li>`).join('') : '<li><p>No timeline has been recorded for this case.</p></li>';
    $('correction-list').innerHTML = (selected.corrections || []).length ? selected.corrections.map((correction) => `<article class="correction" id="correction-${escape(correction.id)}">${badge('recorded correction')}<h3>${escape(correction.from_revision_id)} → ${escape(correction.to_revision_id)}</h3><p>${escape(correction.cause)}</p><blockquote class="before"><span class="change-label">Original published wording</span>${escape(correction.before)}${correction.before_status ? `<br>Status: ${escape(claimStatusName(correction.before_status))}` : ''}</blockquote><blockquote class="after"><span class="change-label">Corrected wording</span>${escape(correction.after)}${correction.after_status ? `<br>Status: ${escape(claimStatusName(correction.after_status))}` : ''}</blockquote><p>Source: ${sourceRefs(correction.source_ids)}</p><a href="#claim-${escape(correction.claim_id)}">Inspect current claim ↑</a></article>`).join('') : '<p class="muted">No correction history has been recorded here. An empty history does not establish that the source material has never changed.</p>';
    $('revision-list').innerHTML = (selected.revisions || []).length ? selected.revisions.map((revision, index) => `<details class="revision" id="revision-${escape(revision.id)}"><summary><strong>${escape(revision.id)}</strong> · ${index === selected.revisions.length - 1 ? 'Current recorded revision' : 'Earlier recorded revision'}<span class="revision-meta">${escape(date(revision.published_at))}</span></summary><div class="revision-body"><p>${escape(revision.change_note)}</p><p>Parent: ${escape(revision.parent_revision_id || 'None — first recorded revision')}<br>Review records: ${(revision.review_ids || []).length ? revision.review_ids.map((id) => `<a href="#review-${escape(id)}">${escape(id)}</a>`).join(', ') : 'None recorded'}</p><ul>${(revision.claim_snapshots || []).map((snapshot) => `<li><strong>${escape(snapshot.claim_id)} · ${escape(claimStatusName(snapshot.status))}</strong><br>${escape(snapshot.text)}</li>`).join('')}</ul></div></details>`).join('') : '<p class="muted">No publication-revision history has been recorded for this case.</p>';
    $('provenance-summary').innerHTML = `<p>${escape(selected.provenance.note)}</p><p>${escape(selected.publication_note)}</p><p><a href="${escape(safeUrl(selected.provenance.url))}">${escape(selected.provenance.label)} ↗</a></p>${selected.source_independence_notes.length ? `<ul>${selected.source_independence_notes.map((note) => `<li>${escape(note)}</li>`).join('')}</ul>` : ''}`;
    $('source-list').innerHTML = selected.sources.map((source) => {
      return `<article class="source-card" id="source-${escape(source.id)}"><span class="source-meta">${escape(source.publisher)} / ${escape(date(source.published_date))}</span><h3>${escape(source.title)}</h3><p class="source-meta">${escape(label(source.source_type))}${source.byline ? ` · ${escape(source.byline)}` : ''}</p><p>${escape(source.notes)}</p>${sourceLink(source, 'Open attributed source ↗')}${publicCopyLinks(source)}<p class="rights">${escape(source.rights)}</p>${sourceChecks(source)}</article>`;
    }).join('');
    $('review-list').innerHTML = (selected.reviews || []).length ? selected.reviews.map((review) => `<article class="review" id="review-${escape(review.id)}"><strong>${escape(review.reviewer)}</strong><p>Decision: ${escape(label(review.decision))}<br>${escape(review.rationale)}</p><p>Conflicts / attribution: ${escape(review.conflicts)}</p></article>`).join('') : '<p class="muted">No named human editorial review or publication approval is recorded for this case. Source-content checks above do not establish an editorial signoff.</p>';
    $('copy-case-link').addEventListener('click', copyCaseLink);
    revealHash(false);
  }

  function renderLedger() {
    const value = $('relationship-filter').value;
    const links = selected.evidence_links.filter((link) => value === 'all' || link.relationship === value);
    $('evidence-body').innerHTML = links.map((link) => {
      const claim = selected.claims.find((item) => item.id === link.claim_id);
      const source = selected.sources.find((item) => item.id === link.source_id);
      return `<tr><td><a href="#claim-${escape(claim.id)}">${escape(claim.id)}</a><p>${escape(claim.kind)}</p></td><td>${badge(link.relationship)}</td><td>${sourceLink(source)}<p>${escape(link.rationale)}</p><p><a href="#source-${escape(source.id)}">Provenance & rights ↓</a></p></td></tr>`;
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
    $('results-count').textContent = 'Loading local case data…';
    $('retry-load').disabled = true;
    try {
      const response = await fetch('./data/cases.json', {cache:'no-store'});
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      if (data.schema_version !== 'spacezh.relay.prototype.v1' || data.prototype !== true || data.confidential_intake !== false || data.trusted_operational_feed !== false || !Array.isArray(data.cases) || !data.cases.length || data.cases.some((item) => !['public_case','public_snapshot'].includes(item.kind))) throw new Error('Invalid public evidence bundle');
      bundle = data;
      renderCheckSummary();
      readLocation();
      renderRegistry();
      revealHash();
    } catch {
      $('case-list').innerHTML = '';
      $('case-workspace').hidden = true;
      $('results-count').textContent = 'Local case data unavailable.';
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
