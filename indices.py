#!/usr/bin/env python2

import re

report_headers = ( 'Score Summary', 'Singapore Student Assessment Information', 'Global Factors', 'Criterion Scores' )

basic_short = {
 'Response Style': ( 'IM', 'IN', 'AC' ), 
 'Global Factors': ( 'G1', 'G2', 'G3', 'G4', 'G5' ),
 '16PF': ( 'A','B','C','E','F','G','H','I','L','M','N','O','Q1','Q2','Q3','Q4' )
}

criterion_short = {
 'Emotional Management': ( 'EM-EM', 'EM-EQ', 'EM-SQ' ),
 'Social Dynamics': ( 'SD-EE', 'SD-ES', 'SD-EC', 'SD-SE', 'SD-SS', 'SD-SC', 'SD-EP' ),
 'Leadership & Enterprising Creativity': ( 'LE-PL', 'LE-PC', 'LE-RO' )
}

composite_short = {
 'Composite Scores': ( 'IC', 'EC' ),
 'Applied Thinking': ( 'AT-CP', 'AT-CA', 'AT-IM', 'AT-XP', 'AT-IN', 'AT-AR', 'AT-IE' ),
 'Motivation to Innovate': ( 'MI-OC', 'MI-RC', 'MI-EN', 'MI-PF', 'MI-UR' ),
 'Educational Style': ( 'ES-SA', 'ES-GP', 'ES-SC' ),
 'Leadership Factors': ( 'LF-LP', 'LF-AL', 'LF-FL', 'LF-PL', 'LF-IF' ),
 'Business Competencies': ( 'BC-EN', 'BC-DP', 'BC-SO', 'BC-RS' )
}

basic_indices = {
 'Response Style': ( 'Impression Management', 'Infrequency', 'Acquiescence' ),
 'Global Factors': ( 'Extraversion', 'Anxiety', 'Tough-Mindedness', 'Independence', 'Self-Control' ),
 '16PF':
	( 'Warmth', 'Reasoning', 'Emotional Stability', 'Dominance',
	'Liveliness', 'Rule-Consciousness', 'Social Boldness', 'Sensitivity',
	'Vigilance', 'Abstractedness', 'Privateness', 'Apprehension',
	'Openness to Change', 'Self-Reliance', 'Perfectionism', 'Tension' ),
}

criterion_indices = {
 'Emotional Management': ( 'Emotional Management', 'Emotional Adversity Quotient', 'Social Adversity Quotient' ),
 'Social Dynamics':
		( 'Emotional Expressivity', 'Emotional Sensitivity', 'Emotional Control', 
		'Social Expressivity', 'Social Sensitivity', 'Social Control', 'Empathy' ),
 'Leadership & Enterprising Creativity':
		( 'potential for leadership', 'potential for creative functioning', 'rate of output' )
}

composite_indices = {
 'Composite Scores': ( 'Innovation Composite', 'Enterprising Composite' ),
 'Applied Thinking': 
		( 'Creative Potential', 'Creative Achievement', 'Imagination', 'Experimenting',
		'Investigative', 'Abstract Reasoning', 'Intellectual Efficiency' ),
 'Motivation to Innovate': ( 'Openness to Change', 'Receptive', 'Energized', 'Perfectionism', 'Unrestrained' ),
 'Educational Style': ( 'School Achievement', 'GPA Potential', 'Self-Confidence' ),
 'Leadership Factors': 
		( 'Leadership Potential', 'Assertive Leadership', 'Facilitative Leadership',
		'Permissive Leadership', 'Influence' ),
 'Business Competencies': ( 'Enterprising', 'Dependability', 'Service Orientation', 'Resilience' )
}

def flatten( d ):
	return [ p for k,x in d.iteritems() for p in x ] 

def search( needle, haystack ):
	try:
		return re.search( needle, haystack ).group(1)
	except AttributeError:
		return ''

def extract( haystack, needles, pre, post ):
	if isinstance( needles, dict ):
		return { k: [ search( pre+t+post, haystack ) for t in x ] for k,x in needles.iteritems() } 
	else:
		return [ search( pre+t+post, haystack ) for t in needles ]

def parse_indices( pages ):
	b_profile = {}
	c_profile = {}
	criterion_scores = {}

	page = [ [ i for i, s in enumerate(pages) if k in s ] for k in report_headers ]

	pf_page = pages[page[0][0]] if page[0] else pages[page[2][0]]

	b_profile['16PF'] = extract( pf_page, basic_indices['16PF'], r'(1?\d) ', '' )

	if page[1]:
		pf_page = ''.join([ pages[x] for x in page[1] ])
		c_profile = extract( pf_page, composite_indices, '', r' (1?\d.\d)' )

	if page[2]:
		pf_page = pages[page[2][0]]
		b_profile['Response Style'] = extract( pf_page, basic_indices['Response Style'], '', r' (\d?\d)' )
		b_profile['Global Factors'] = extract( pf_page, basic_indices['Global Factors'], r'(1?\d) ', '' )

	if page[3]:
		compositepage = re.sub( r'.*Criterion Scores.*', '', ''.join([ pages[x] for x in page[3] ]) )
		verbose_report = ' '.join( re.sub( r'\s\s\d\s\s', r'', compositepage ).split() )

		ci = { k: [ re.sub(' ',' ?',t) for t in x ] for k,x in criterion_indices.iteritems() }
		criterion_scores = extract( verbose_report, ci, '', r'.*?\((1?\d)\).' )

	return ( b_profile, c_profile, criterion_scores )

if __name__ == "__main__": pass
