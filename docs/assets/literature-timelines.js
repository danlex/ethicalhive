(function () {
  'use strict';
  var dataPromise;
  var serial = 0;
  var number = new Intl.NumberFormat('en');
  var SVG = 'http://www.w3.org/2000/svg';

  function element(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function svg(tag, attrs, text) {
    var node = document.createElementNS(SVG, tag);
    Object.keys(attrs || {}).forEach(function (key) { node.setAttribute(key, attrs[key]); });
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function dataset() {
    if (!dataPromise) {
      dataPromise = fetch('literature-timelines.json').then(function (response) {
        if (!response.ok) throw new Error('Timeline data unavailable');
        return response.json();
      }).then(function (data) {
        if (data.schema_version !== 1 || !Array.isArray(data.records)) throw new Error('Invalid timeline format');
        data.byId = new Map(data.records.map(function (record) { return [record.id, record]; }));
        return data;
      }).catch(function (error) { dataPromise = null; throw error; });
    }
    return dataPromise;
  }

  function sourceURL(record, year) {
    var query = record.query;
    if (year !== undefined) query = '(' + query + ') AND submittedDate:[' + year + '01010000 TO ' + year + '12312359]';
    var url = new URL('https://export.arxiv.org/api/query');
    url.searchParams.set('search_query', query);
    url.searchParams.set('max_results', '25');
    url.searchParams.set('sortBy', 'submittedDate');
    url.searchParams.set('sortOrder', 'descending');
    return url.href;
  }

  function link(text, url) {
    var node = element('a', '', text);
    node.href = url;
    node.target = '_blank';
    node.rel = 'noopener';
    return node;
  }

  function choose(label, options, className) {
    var wrapper = element('label', '', label + ' ');
    var select = element('select', className);
    options.forEach(function (option) {
      var node = element('option', '', option[1]); node.value = option[0]; select.appendChild(node);
    });
    wrapper.appendChild(select);
    return {label: wrapper, select: select};
  }

  function validate(record) {
    if (!record || record.status !== 'complete' || !Array.isArray(record.years)) return false;
    var sum = 0;
    if (record.years.length !== record.end_year - record.start_year + 1) return false;
    for (var i = 0; i < record.years.length; i++) {
      var point = record.years[i];
      if (point.year !== record.start_year + i || !Number.isSafeInteger(point.count) || point.count < 0) return false;
      sum += point.count;
    }
    return sum === record.total;
  }

  function render(widget, record, data) {
    var mount = widget.querySelector('.timeline-mount');
    mount.replaceChildren();
    if (!validate(record)) {
      mount.appendChild(element('p', 'timeline-note', 'A complete yearly series is not available for this search. Missing data is not shown as zero.'));
      widget.dataset.timelineState = 'unavailable';
      return;
    }
    widget.dataset.timelineState = 'ready';
    var controls = element('div', 'timeline-controls');
    var period = choose('Years', [['all', 'All available years'], ['recent', 'Last 10 years'], ['2000', 'Since 2000']], 'timeline-period');
    var scale = choose('Scale', [['linear', 'Linear'], ['log', 'Logarithmic']], 'timeline-scale');
    controls.append(period.label, scale.label);
    mount.appendChild(controls);
    var chart = svg('svg', {viewBox: '0 0 600 250', class: 'timeline-plot', role: 'group', tabindex: '0'});
    var helpId = 'timeline-help-' + (++serial);
    chart.setAttribute('aria-label', record.name + ': yearly matching publications');
    chart.setAttribute('aria-describedby', helpId);
    mount.appendChild(element('p', 'timeline-sr-only', 'Use Left and Right arrow keys to inspect a year. Exact values are also in the annual data table.'));
    mount.lastChild.id = helpId;
    mount.appendChild(chart);
    var readout = element('div', 'timeline-readout');
    var output = element('output'); output.setAttribute('aria-live', 'polite');
    var yearLink = link('View this year’s source query', sourceURL(record));
    readout.append(output, yearLink); mount.appendChild(readout);
    mount.appendChild(element('p', 'timeline-note', 'Checked ' + record.queried_at.slice(0, 10) + '. ' + record.end_year + ' is an incomplete year in this snapshot; its bar is outlined.'));
    if (record.total === 0) mount.appendChild(element('p', '', 'No publications matched this search in the recorded interval. This does not establish that the behaviour is absent or unstudied.'));
    var tableDetails = element('details', 'timeline-data');
    tableDetails.appendChild(element('summary', '', 'Annual data table'));
    var tableWrap = element('div', 'timeline-table-wrap');
    var table = element('table');
    var caption = element('caption', 'timeline-sr-only', record.name + ': matching arXiv publications by first-submission year');
    table.appendChild(caption);
    var head = element('thead'); var headRow = element('tr');
    ['Year', 'Matching publications'].forEach(function (text) { var th = element('th', '', text); th.scope = 'col'; headRow.appendChild(th); });
    head.appendChild(headRow); table.appendChild(head);
    var tbody = element('tbody'); table.appendChild(tbody);
    tableWrap.appendChild(table); tableDetails.appendChild(tableWrap); mount.appendChild(tableDetails);
    var source = element('details', 'timeline-source');
    source.appendChild(element('summary', '', 'Source, dates and search scope'));
    source.appendChild(element('p', '', 'arXiv · cs.AI, cs.CL and cs.LG · first-submission year. Each matching publication is counted once, not each occurrence of a word.'));
    source.appendChild(element('p', '', 'This AI-domain search does not cover all psychology or psychotherapy research. A zero count only describes this query, scope and retrieval date.'));
    source.appendChild(element('p', '', 'Keyword matches can be incidental. Searches use currently indexed versions: a later revision can introduce a term into a paper with an older first-submission date. These are not dates of a term’s first use.'));
    var date = record.queried_at ? record.queried_at.slice(0, 10) : 'not recorded';
    source.appendChild(element('p', '', 'Yearly snapshot checked ' + date + '.'));
    if (record.historical_zero_snapshot) source.appendChild(element('p', '', 'This reuses the existing zero-result search at its original date. Its recorded total of zero establishes every annual value in that interval.'));
    if (record.catalogue_queried_at && record.catalogue_queried_at.slice(0, 10) !== date) {
      source.appendChild(element('p', '', 'The catalogue row total was checked ' + record.catalogue_queried_at.slice(0, 10) + '; different retrieval dates can give different totals.'));
    }
    source.appendChild(element('code', '', record.query));
    source.appendChild(link('Open the complete source query', sourceURL(record)));
    mount.appendChild(source);
    var visible = [], selected = -1, bars = [], renderedWidth = 0;

    function inspect(index) {
      selected = Math.max(0, Math.min(index, visible.length - 1));
      var point = visible[selected];
      output.textContent = point.year + ': ' + number.format(point.count) + ' matching publication' + (point.count === 1 ? '' : 's') + (point.year === record.end_year ? ' · partial year' : '');
      yearLink.href = sourceURL(record, point.year);
      bars.forEach(function (bar, i) { bar.classList.toggle('timeline-selected', i === selected); });
    }

    function draw() {
      var lower = period.select.value === 'recent' ? record.end_year - 9 : (period.select.value === '2000' ? 2000 : record.start_year);
      visible = record.years.filter(function (point) { return point.year >= lower; });
      chart.replaceChildren(svg('title', {}, record.name + ': matching publications per year'));
      bars = [];
      renderedWidth = Math.max(220, Math.round(mount.getBoundingClientRect().width));
      chart.setAttribute('viewBox', '0 0 ' + renderedWidth + ' 250');
      var left = 52, top = 25, width = renderedWidth - 68, height = 184, bottom = top + height;
      var maximum = Math.max.apply(null, visible.map(function (point) { return point.count; }).concat([1]));
      var logarithmic = scale.select.value === 'log';
      var magnitude = Math.pow(10, Math.floor(Math.log10(Math.max(1, maximum / 4))));
      var ratio = Math.max(1, maximum / 4) / magnitude;
      var step = (ratio <= 1 ? 1 : ratio <= 2 ? 2 : ratio <= 5 ? 5 : 10) * magnitude;
      var maxValue = logarithmic ? Math.pow(10, Math.ceil(Math.log10(maximum))) : Math.ceil(maximum / step) * step;
      function y(value) { return bottom - height * (logarithmic ? Math.log10(value + 1) / Math.log10(maxValue + 1) : value / maxValue); }
      var ticks = [0];
      if (logarithmic) { for (var value = 1; value <= maxValue; value *= 10) ticks.push(value); }
      else { for (var tick = step; tick <= maxValue; tick += step) ticks.push(tick); }
      ticks.forEach(function (value) {
        chart.append(svg('line', {x1:left, x2:left + width, y1:y(value), y2:y(value), class:'timeline-grid'}));
        chart.append(svg('text', {x:left - 8, y:y(value) + 4, 'text-anchor':'end'}, number.format(value)));
      });
      chart.appendChild(svg('text', {x:left, y:15}, 'Publications'));
      var cell = width / visible.length;
      visible.forEach(function (point, i) {
        var x = left + cell * i;
        var bar = svg('rect', {x:x + cell * .12, y:y(point.count), width:cell * .76,
          height:Math.max(0, bottom - y(point.count)), class:'timeline-bar' + (point.year === record.end_year ? ' timeline-current' : '')});
        bar.appendChild(svg('title', {}, point.year + ': ' + number.format(point.count)));
        chart.appendChild(bar); bars.push(bar);
        var hit = svg('rect', {x:x, y:top, width:cell, height:height, class:'timeline-hit', 'data-year':point.year});
        hit.addEventListener('pointerenter', function () { inspect(i); });
        hit.addEventListener('click', function () { inspect(i); });
        chart.appendChild(hit);
        var labelEvery = Math.max(1, Math.ceil(visible.length / Math.max(2, Math.floor(width / 65))));
        var interiorLabel = i % labelEvery === 0 && i * cell >= 55 && (visible.length - 1 - i) * cell >= 55;
        if (i === 0 || i === visible.length - 1 || interiorLabel) {
          chart.appendChild(svg('text', {x:x + cell / 2, y:bottom + 22, 'text-anchor':'middle', class:'timeline-year-label'}, point.year + (point.year === record.end_year ? '*' : '')));
        }
      });
      tbody.replaceChildren();
      visible.slice().reverse().forEach(function (point) {
        var row = element('tr'); var year = element('td');
        year.appendChild(link(String(point.year) + (point.year === record.end_year ? '*' : ''), sourceURL(record, point.year)));
        row.append(year, element('td', '', number.format(point.count))); tbody.appendChild(row);
      });
      var last = visible.length - 1;
      while (last > 0 && visible[last].count === 0) last--;
      inspect(last);
    }
    chart.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault(); inspect(selected + (event.key === 'ArrowRight' ? 1 : -1));
      } else if (event.key === 'Home' || event.key === 'End') {
        event.preventDefault(); inspect(event.key === 'Home' ? 0 : visible.length - 1);
      }
    });
    period.select.addEventListener('change', draw);
    scale.select.addEventListener('change', draw);
    if ('ResizeObserver' in window) new ResizeObserver(function (entries) {
      var width = Math.round(entries[0].contentRect.width);
      if (width > 0 && width !== renderedWidth) draw();
    }).observe(mount);
    draw();
  }

  function load(widget) {
    if (widget.dataset.timelineState) return;
    widget.dataset.timelineState = 'loading';
    var mount = widget.querySelector('.timeline-mount');
    mount.replaceChildren(element('p', '', 'Loading yearly search data…'));
    dataset().then(function (data) { render(widget, data.byId.get(widget.dataset.timelineTerm), data); }).catch(function () {
      widget.dataset.timelineState = 'error';
      mount.replaceChildren(element('p', '', 'Yearly data could not be loaded. No counts have been inferred.'));
      var retry = element('button', 'timeline-retry', 'Retry'); retry.type = 'button';
      retry.addEventListener('click', function () { delete widget.dataset.timelineState; load(widget); });
      mount.appendChild(retry);
    });
  }

  var observer = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting && entry.target.closest('details.concept').open) { observer.unobserve(entry.target); load(entry.target); }
    });
  }, {rootMargin:'200px'}) : null;

  function opened(box) {
    if (!box.open) return;
    var widget = box.querySelector('.literature-timeline');
    if (!widget || widget.dataset.timelineState) return;
    if (observer) observer.observe(widget); else load(widget);
  }
  document.addEventListener('toggle', function (event) { if (event.target.matches('details.concept')) opened(event.target); }, true);
  document.querySelectorAll('details.concept[open]').forEach(opened);
})();
