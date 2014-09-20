"""
Alexander Groden

Created as the solution to an assignment in:
CYB5678 - Cryptography and Information Hiding
"""

from collections import defaultdict
import htree as h

verbose = False


def modify_codes(t, n):
	same0 = '0' * n
	greater0 = '0' * (n + 1)
	lesser0 = '0' * (n - 1)
	same1 = '1' * n
	greater1 = '1' * (n + 1)
	lesser1 = '1' * (n - 1)
	def recurse(t):
		for key in t.keys():
			old_key = key.split(':')
			if len(old_key) == 3 and old_key[0] != '*':
				if len(old_key[2]) >= n and old_key[2].endswith(same0):
					if t[key]:
						recurse(t[key])
				elif len(old_key[2]) >= n and old_key[2].endswith(same1):
					if t[key]:
						recurse(t[key])
				#elif len(old_key[2]) >= n+1 and old_key[2][-(n+1):] == greater0:
				elif len(old_key[2]) >= n + 1 and old_key[2].endswith(greater0):
					if verbose:
						print 'code for "%s" ends with more than %d zeros, adding "010"' % (old_key[0], n)
					code = ''.join([old_key[2], '010'])
					new_key = ''.join([old_key[0], ':', old_key[1], ':', code])
					t[new_key] = t.pop(key)
					if t[new_key]:
						recurse(t[new_key])
				#elif len(old_key[2]) >= n+1 and old_key[2][-(n+1):] == greater1:
				elif len(old_key[2]) >= n + 1 and old_key[2].endswith(greater1):
					if verbose:
						print 'code for "%s" ends with more than %d ones, doing nothing' % (old_key[0], n)
					if t[key]:
						recurse(t[key])
				#elif len(old_key[2]) > n and old_key[2][-(n-1):] == lesser0:
				elif len(old_key[2]) >= n - 1 and old_key[2].endswith(lesser0):
					if verbose:
						print 'code for "%s" ends with less than %d zeros, adding "1"' % (old_key[0], n)
					code = ''.join([old_key[2], '1'])
					new_key = ''.join([old_key[0], ':', old_key[1], ':', code])
					t[new_key] = t.pop(key)
					if t[new_key]:
						recurse(t[new_key])
				#elif len(old_key[2]) > n and old_key[2][-(n-1):] == lesser1:
				elif len(old_key[2]) >= n - 1 and old_key[2].endswith(lesser1):
					if verbose:
						print 'code for "%s" ends with less than %d ones, adding "01"' % (old_key[0], n)
					code = ''.join([old_key[2], '01'])
					new_key = ''.join([old_key[0], ':', old_key[1], ':', code])
					t[new_key] = t.pop(key)
					if t[new_key]:
						recurse(t[new_key])
				else:
					if t[key]:
						recurse(t[key])
			elif t[key]:
				recurse(t[key])
	recurse(t)


def encode(t, s, sync):
	ret = sync
	if verbose:
		print '#: %s' % (sync,)
	for c in s:
		if verbose:
			print '%s: %s' % (c, h.get_code(t, c))
		ret = ''.join([ret, h.get_code(t, c)])
	if verbose:
		print '#: %s' % (sync,)
	ret = ''.join([ret, sync])
	return ret


def main(args):
	global verbose
	verbose = args.verbose
	f = h.freq(args.string)
	print 'tree node structure: character (or * for joiner):frequency:binary code'
	if verbose:
		print 'frequency table:'
	for key, value in sorted(f.items(), key=lambda x:(x[1], x[0])):
		if verbose:
			print '  %d: "%s"' % (value, key)
	if verbose:
		print
		print 'generating huffman tree...'
	t = h.htree(freq=f, verbose=args.verbose)
	if verbose:
		print
		print 'done generating huffman tree:'
		h.print_tree(t)
		print
		print 'adding 2n sync codes...'
	else:
		print 'base huffman tree:'
		h.print_tree(t)
	depth = h.depth(t)
	n = depth / 2
	sync_code = ''.join(['0' * n, '1' * n])
	if verbose:
		print 'depth (%d) / 2 = n (%d)' % (depth, n)
	print '\nsync code: %s' % (sync_code,)
	if verbose:
		print
		print 'modifying codes...'
	modify_codes(t, n)
	print '\nmodified huffman tree:'
	h.print_tree(t)
	if verbose:
		print
		print 'encoding string...'
	print '\nencoded string:\n%s' % (encode(t, args.string, sync_code))


if __name__ == '__main__':
	from argparse import ArgumentParser
	import sys
	parser = ArgumentParser(
		description='')
	parser.add_argument('string', type=str, help='the string to code')
	parser.add_argument('--verbose', '-v', default=False, action='store_true',
		help='show work')
	sys.exit(main(parser.parse_args()))
