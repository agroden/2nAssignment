"""
Alexander Groden

Implementation of a minimal Huffman tree
"""

from collections import defaultdict

def freq(s):
	'''
	Generate a frequency table given a string.
	'''
	ret = {}
	for c in s:
		if c in ret.keys():
			ret[c] += 1
		else:
			ret[c] = 1
	return ret


def tree():
	"""
	A dictionary backed tree. About as Pythonic as it gets.
	"""
	return defaultdict(tree)


def print_tree(t):
	"""
	Pretty prints the tree. Indention indicates tree levels, higher in the 
	list indicates the item is to the left, while the last entries in the list
	indicate the item is to the right.
	"""
	def sort_by(x):
		y = x.split(':')
		return (int(y[1]), y[0])
	def recurse(t, prefix = ''):
		for key in sorted(t.keys(), key=sort_by):
			print '{}{}'.format(prefix, key)
			if t[key]:
				recurse(t[key], prefix + '  |')
	recurse(t, '')


def depth(t):
	'''
	Returns the depth of the given tree.
	'''
	ret = [0,]
	def recurse(t, d):
		if d > ret[0]:
			ret[0] = d
		for key in t.keys():
			if t[key]:
				recurse(t[key], d + 1)
		return d
	recurse(t, ret[0])
	return ret[0]


def get_code(t, c):
	'''
	Returns the code for the given character.
	'''
	def sort_by(x):
		y = x.split(':')
		return (int(y[1]), y[0])
	code = ['']
	def recurse(t):
		for key in sorted(t.keys(), key=sort_by):
			k = key.split(':')
			if k[0] == c:
				code[0] = k[2]
			elif t[key]:
				recurse(t[key])
	recurse(t)
	return code[0]


def htree(freq=(), s='', verbose=False):
	'''
	Generate a huffman tree given a frequency table.
	'''
	def add_to_tree(t, val, freq):
		new_tree = tree()
		root = make_node(['*', freq])
		new_tree[root][make_node(val)]
		new_tree[root][t.keys()[0]] = t[t.keys()[0]]
		return new_tree

	def merge_trees(t1, t2, freq):
		new_tree = tree()
		root = make_node(['*', freq])
		new_tree[root][t1.keys()[0]] = t1[t1.keys()[0]]
		new_tree[root][t2.keys()[0]] = t2[t2.keys()[0]]
		return new_tree

	def make_node(val):
		return ''.join([val[0], ':', str(val[1])])

	if not freq:
		freq = freq(s)
	ts = {}
	f = sorted(freq.items(), key=lambda x:(x[1], x[0]))
	while len(f) != 1:
		l = f.pop(0)
		r = f.pop(0)
		new_freq = l[1] + r[1]
		if l[0] == '*':
			if r[0] == '*': # both the left and right nodes are in the trees list
				new_tree = merge_trees(ts[make_node(l)], ts[make_node(r)], new_freq)
				del ts[make_node(l)]
				del ts[make_node(r)]
				ts[new_tree.keys()[0]] = new_tree
				if verbose:
					print
					print 'merging disjoint trees:'
					print_tree(new_tree)
			else: # the left node is in the trees list
				new_tree = add_to_tree(ts[make_node(l)], l, new_freq)
				del ts[make_node(l)]
				ts[new_tree.keys()[0]] = new_tree
				if verbose:
					print
					print 'adding to tree on the right:'
					print_tree(new_tree)
		elif r[0] == '*': # the right node is in the trees list
			new_tree = add_to_tree(ts[make_node(r)], r, new_freq)
			new_tree[make_node(('*', new_freq))][make_node(l)]
			del ts[make_node(r)]
			ts[new_tree.keys()[0]] = new_tree
			if verbose:
				print
				print 'adding to tree on the left:'
				print_tree(new_tree)
		else: # neither node is in the trees list
			new_tree = tree()
			root = make_node(['*', new_freq])
			new_tree[root][make_node(l)]
			new_tree[root][make_node(r)]
			ts[new_tree.keys()[0]] = new_tree
			if verbose:
				print
				print 'new tree:'
				print_tree(new_tree)
		# add new freq back in
		f.append(('*', new_freq))
		f = sorted(f, key=lambda x:(x[1], x[0]))
	final_tree = ts[make_node(f[0])]
	return add_codes(final_tree)


def add_codes(base_tree):
	'''
	Adds the binary Huffman codes to the tree
	'''
	coded_tree = tree()
	root = base_tree.keys()[0]
	coded_tree[root]
	def sort_by(x):
		y = x.split(':')
		return (int(y[1]), y[0])
	def add_code(c, b, code = ''):
		for idx, key in enumerate(sorted(b.keys(), key=sort_by)):
			new_code = ''.join([code, str(idx)])
			new_key = ''.join([key, ':', new_code])
			c[new_key]
			if b[key]:
				add_code(c[new_key], b[key], new_code)
	add_code(coded_tree[root], base_tree[root])
	return coded_tree
