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
    if (url.charAt(0) !== '#') { node.target = '_blank'; node.rel = 'noopener'; }
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

  function renderOverview(widget, data) {
    var mount = widget.querySelector('.overview-mount');
    mount.replaceChildren();
    var records = data.records.filter(validate);
    if (!records.length) {
      widget.dataset.overviewState = 'unavailable';
      mount.appendChild(element('p', '', 'Complete yearly series are unavailable. Missing data is not shown as zero.'));
      return;
    }
    var byId = new Map(records.map(function (record) {
      record.points = new Map(record.years.map(function (point) { return [point.year, point.count]; }));
      return [record.id, record];
    }));
    var ranked = records.slice().sort(function (a, b) { return b.total - a.total || a.name.localeCompare(b.name); });
    var selected = ranked.slice(0, 5).map(function (record) { return record.id; });
    var colors = ['#6554d9', '#007b83', '#b74413', '#a72a85', '#386fb4', '#64731d'];
    var controls = element('div', 'timeline-controls');
    var mode = choose('View', [['combined', 'All terms combined'], ['compare', 'Compare terms']], 'overview-mode');
    var period = choose('Years', [['all', 'All available years'], ['recent', 'Last 10 years'], ['2000', 'Since 2000']], 'overview-period');
    var scale = choose('Scale', [['linear', 'Linear'], ['log', 'Logarithmic']], 'overview-scale');
    controls.append(mode.label, period.label, scale.label); mount.appendChild(controls);
    var picker = element('div', 'overview-picker'); picker.hidden = true;
    var searchLabel = element('label', '', 'Find a term');
    var search = element('input', 'overview-search'); search.type = 'search';
    search.placeholder = 'Search terms to compare'; searchLabel.appendChild(search); picker.appendChild(searchLabel);
    var available = element('select', 'overview-available'); available.setAttribute('aria-label', 'Term to add');
    var add = element('button', 'overview-add', 'Add term'); add.type = 'button';
    picker.append(available, add);
    var chips = element('div', 'overview-selected'); picker.appendChild(chips);
    var selectionNote = element('p', 'timeline-note'); selectionNote.setAttribute('aria-live', 'polite'); picker.appendChild(selectionNote);
    mount.appendChild(picker);
    var chart = svg('svg', {viewBox:'0 0 800 300', class:'timeline-plot overview-plot', role:'group', tabindex:'0',
      'aria-label':'Yearly arXiv research across catalogue terms', 'aria-describedby':'overview-keyboard-help'});
    var help = element('p', 'timeline-sr-only', 'Use Left and Right arrows to inspect a year, or Home and End. Exact values are in the table.');
    help.id = 'overview-keyboard-help'; mount.append(help, chart);
    var output = element('output', 'overview-readout'); output.setAttribute('aria-live', 'polite'); mount.appendChild(output);
    var values = element('ul', 'overview-values'); mount.appendChild(values);
    var coverage = element('p', 'timeline-note overview-coverage'); mount.appendChild(coverage);
    var dates = records.map(function (record) { return record.queried_at.slice(0, 10); }).sort();
    mount.appendChild(element('p', 'timeline-note', 'arXiv · cs.AI, cs.CL and cs.LG · first-submission year. Search dates: ' +
      dates[0] + (dates[0] === dates[dates.length - 1] ? '' : ' to ' + dates[dates.length - 1]) +
      '. The retrieval year is incomplete (*). Indexed revisions can introduce a term into an older submission cohort.'));
    var tableDetails = element('details', 'timeline-data overview-data');
    tableDetails.appendChild(element('summary', '', 'Annual data table'));
    var tableWrap = element('div', 'timeline-table-wrap');
    var table = element('table'); var caption = element('caption', 'timeline-sr-only', 'Yearly search-match values for the current chart');
    var head = element('thead'); var body = element('tbody'); table.append(caption, head, body);
    tableWrap.appendChild(table); tableDetails.appendChild(tableWrap); mount.appendChild(tableDetails);
    var visible = [], active = [], points = [], inspected = -1, drawnWidth = 0;

    function updatePicker() {
      var query = search.value.trim().toLowerCase();
      available.replaceChildren();
      records.slice().sort(function (a, b) { return a.name.localeCompare(b.name); }).forEach(function (record) {
        if (selected.indexOf(record.id) !== -1 || record.name.toLowerCase().indexOf(query) === -1) return;
        var option = element('option', '', record.name); option.value = record.id; available.appendChild(option);
      });
      add.disabled = selected.length >= colors.length || !available.options.length;
      chips.replaceChildren();
      selected.forEach(function (id, index) {
        var remove = element('button', 'overview-chip', byId.get(id).name + ' ×'); remove.type = 'button';
        remove.style.setProperty('--series-color', colors[index]);
        remove.setAttribute('aria-label', 'Remove ' + byId.get(id).name);
        remove.addEventListener('click', function () { selected = selected.filter(function (value) { return value !== id; }); updatePicker(); draw(); });
        chips.appendChild(remove);
      });
      selectionNote.textContent = selected.length + ' of ' + colors.length + ' comparison slots used. ' +
        (!available.options.length ? 'No other terms match this search.' : selected.length >= colors.length ?
          'Remove a term to free a slot.' : 'Choose a term and select Add term.');
    }

    function inspect(index) {
      if (!points.length) return;
      inspected = Math.max(0, Math.min(index, points.length - 1));
      var point = points[inspected];
      output.textContent = point.year + (point.partial ? ' · partial year' : '') + (mode.select.value === 'combined' ?
        ': ' + (point.covered ? number.format(point.total) + ' paper–term matches' : 'data unavailable') : ' · term comparison');
      values.replaceChildren();
      if (mode.select.value === 'compare') active.forEach(function (record, i) {
        var count = record.points.get(point.year);
        var item = element('li', '', record.name + ': ' + (count === undefined ? 'unavailable' : number.format(count)));
        item.style.setProperty('--series-color', colors[i]);
        item.appendChild(link('Details', '#' + record.id)); values.appendChild(item);
      });
      chart.querySelectorAll('[data-year]').forEach(function (bar) { bar.classList.toggle('timeline-selected', Number(bar.dataset.year) === point.year); });
    }

    function draw() {
      var compare = mode.select.value === 'compare'; picker.hidden = !compare;
      active = compare ? selected.map(function (id) { return byId.get(id); }) : records;
      var lower = period.select.value === 'recent' ? data.end_year - 9 : (period.select.value === '2000' ? 2000 : data.start_year);
      visible = []; for (var year = lower; year <= data.end_year; year++) visible.push(year);
      points = visible.map(function (year) {
        var point = {year:year, total:0, covered:0, partial:false};
        active.forEach(function (record) {
          if (!record.points.has(year)) return;
          point.total += record.points.get(year); point.covered++;
          if (year === record.end_year) point.partial = true;
        });
        return point;
      });
      chart.replaceChildren(svg('title', {}, compare ? 'Compare annual search matches by term' : 'Combined yearly paper–term search matches'));
      drawnWidth = Math.max(260, Math.round(mount.getBoundingClientRect().width));
      chart.setAttribute('viewBox', '0 0 ' + drawnWidth + ' 300');
      var left = 62, width = drawnWidth - 82, top = 30, height = 215, bottom = top + height;
      var maximum = 1;
      if (compare) active.forEach(function (record) { visible.forEach(function (year) {
        maximum = Math.max(maximum, record.points.get(year) || 0);
      }); });
      if (!compare) maximum = Math.max.apply(null, points.map(function (point) { return point.total; }).concat([1]));
      var log = scale.select.value === 'log';
      var magnitude = Math.pow(10, Math.floor(Math.log10(Math.max(1, maximum / 4))));
      var ratio = Math.max(1, maximum / 4) / magnitude;
      var step = (ratio <= 1 ? 1 : ratio <= 2 ? 2 : ratio <= 5 ? 5 : 10) * magnitude;
      var ceiling = log ? Math.pow(10, Math.ceil(Math.log10(maximum))) : Math.ceil(maximum / step) * step;
      function y(value) { return bottom - height * (log ? Math.log10(value + 1) / Math.log10(ceiling + 1) : value / ceiling); }
      var ticks = [0];
      if (log) { for (var value = 1; value <= ceiling; value *= 10) ticks.push(value); }
      else { for (var tick = step; tick <= ceiling; tick += step) ticks.push(tick); }
      ticks.forEach(function (value) {
        chart.append(svg('line', {x1:left, x2:left + width, y1:y(value), y2:y(value), class:'timeline-grid'}),
          svg('text', {x:left - 8, y:y(value) + 4, 'text-anchor':'end'}, number.format(value)));
      });
      chart.appendChild(svg('text', {x:left, y:17}, compare ? 'Publications per term' : 'Paper–term matches'));
      var cell = width / visible.length;
      function x(index) { return left + cell * (index + .5); }
      if (compare) active.forEach(function (record, i) {
        var segments = [], segment = [];
        visible.forEach(function (year, index) {
          var count = record.points.get(year);
          if (count === undefined) { if (segment.length) segments.push(segment); segment = []; return; }
          segment.push(x(index) + ',' + y(count));
          var dot = svg('circle', {cx:x(index), cy:y(count), r:year === record.end_year ? 3.5 : 2,
            fill:year === record.end_year ? '#fff' : colors[i], stroke:colors[i], 'stroke-width':1.5, class:'overview-point'});
          dot.appendChild(svg('title', {}, record.name + ', ' + year + ': ' + number.format(count))); chart.appendChild(dot);
        });
        if (segment.length) segments.push(segment);
        segments.forEach(function (part) { chart.appendChild(svg('polyline', {points:part.join(' '), fill:'none', stroke:colors[i], 'stroke-width':2, class:'overview-line'})); });
      });
      points.forEach(function (point, i) {
        if (!compare && point.covered) chart.appendChild(svg('rect', {x:left + cell * (i + .12), y:y(point.total), width:cell * .76,
          height:bottom - y(point.total), class:'timeline-bar' + (point.partial ? ' timeline-current' : ''), 'data-year':point.year}));
        var hit = svg('rect', {x:left + cell * i, y:top, width:cell, height:height, class:'timeline-hit'});
        hit.addEventListener('pointerenter', function () { inspect(i); }); hit.addEventListener('click', function () { inspect(i); }); chart.appendChild(hit);
        var every = Math.max(1, Math.ceil(visible.length / Math.max(2, Math.floor(width / 65))));
        if (i === 0 || i === visible.length - 1 || (i % every === 0 && i * cell >= 55 && (visible.length - 1 - i) * cell >= 55))
          chart.appendChild(svg('text', {x:x(i), y:bottom + 25, 'text-anchor':'middle', class:'timeline-year-label'}, point.year + (point.partial ? '*' : '')));
      });
      head.replaceChildren(); body.replaceChildren();
      var row = element('tr'); ['Year'].concat(compare ? active.map(function (record) { return record.name; }) : ['Paper–term matches', 'Covered searches']).forEach(function (text) {
        var th = element('th', '', text); th.scope = 'col'; row.appendChild(th);
      }); head.appendChild(row);
      points.slice().reverse().forEach(function (point) {
        var tr = element('tr'); tr.appendChild(element('td', '', point.year + (point.partial ? '*' : '')));
        var counts = compare ? active.map(function (record) { var count = record.points.get(point.year); return count === undefined ? 'unavailable' : number.format(count); }) :
          [point.covered ? number.format(point.total) : 'unavailable', String(point.covered)];
        counts.forEach(function (value) { tr.appendChild(element('td', '', value)); }); body.appendChild(tr);
      });
      var unavailable = data.records.length - records.length;
      coverage.textContent = (compare && !active.length ? 'Choose a term to display. ' : '') +
        (unavailable ? unavailable + ' searches lack complete data and are excluded. ' : 'All catalogue searches have complete series for their recorded dates. ') +
        'Missing years are unavailable, not zero.' + (log ? ' Logarithmic scale uses log10(1 + count).' : '');
      inspect(inspected < 0 ? points.length - 1 : Math.min(inspected, points.length - 1));
    }
    chart.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight' || event.key === 'Home' || event.key === 'End') {
        event.preventDefault(); inspect(event.key === 'Home' ? 0 : event.key === 'End' ? points.length - 1 : inspected + (event.key === 'ArrowRight' ? 1 : -1));
      }
    });
    search.addEventListener('input', updatePicker);
    add.addEventListener('click', function () { if (!add.disabled) { selected.push(available.value); updatePicker(); draw(); } });
    [mode.select, period.select, scale.select].forEach(function (control) { control.addEventListener('change', draw); });
    if ('ResizeObserver' in window) new ResizeObserver(function (entries) {
      var width = Math.round(entries[0].contentRect.width); if (width > 0 && width !== drawnWidth) draw();
    }).observe(mount);
    updatePicker(); draw(); widget.dataset.overviewState = 'ready';
  }

  var overview = document.getElementById('research-timeline');
  function loadOverview() {
    if (!overview || overview.dataset.overviewState) return;
    overview.dataset.overviewState = 'loading';
    var mount = overview.querySelector('.overview-mount'); mount.replaceChildren(element('p', '', 'Loading research timeline…'));
    dataset().then(function (data) { renderOverview(overview, data); }).catch(function () {
      overview.dataset.overviewState = 'error';
      mount.replaceChildren(element('p', '', 'Research timeline could not be loaded. No counts have been inferred.'));
      var retry = element('button', 'timeline-retry', 'Retry'); retry.type = 'button';
      retry.addEventListener('click', function () { delete overview.dataset.overviewState; loadOverview(); }); mount.appendChild(retry);
    });
  }
  if (overview) {
    if ('IntersectionObserver' in window) {
      var overviewObserver = new IntersectionObserver(function (entries) {
        if (entries.some(function (entry) { return entry.isIntersecting; })) { overviewObserver.disconnect(); loadOverview(); }
      }, {rootMargin:'200px'});
      overviewObserver.observe(overview);
    } else loadOverview();
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
