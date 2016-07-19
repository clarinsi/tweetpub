#!/usr/bin/python
import Levenshtein
import argparse
import sys

def lcs(s1,s2):
  m=[[0]*(1+len(s2)) for i in xrange(1+len(s1))]
  longest,x_longest,y_longest = 0,0,0
  for x in xrange(1,1+len(s1)):
    for y in xrange(1,1+len(s2)):
      if s1[x-1]==s2[y-1]:
        m[x][y]=m[x-1][y-1]+1
        if m[x][y]>longest:
          longest=m[x][y]
          x_longest=x
          y_longest=y
      else:
        m[x][y]=0
  return s1[x_longest-longest:x_longest],x_longest,y_longest

def extract_rule(token,value):
  base,end_token,end_value=lcs(token,value)
  start_token=end_token-len(base)
  start_value=end_value-len(base)
  return start_token,value[:start_value],len(token)-end_token,value[end_value:]

if __name__=='__main__':
  parser=argparse.ArgumentParser(description='Encoder of annotated tweet collections into a shareable format.')
  parser.add_argument('--ncol',help='number of columns in lines representing tokens',type=int,required=True)
  parser.add_argument('--tokencol',help='index of column containing the token, default is 1',type=int,default=1)
  parser.add_argument('--to_encode',help='indices of columns to be encoded relative to the token column',type=int,nargs='+')
  args=parser.parse_args()
  if args.to_encode!=None:
    for i in range(len(args.to_encode)):
      args.to_encode[i]-=1
  args.tokencol-=1
  for line in sys.stdin:
    els=line[:-1].decode('utf8').split('\t')
    if len(els)==args.ncol:
      out=''
      for index in range(len(els)):
        if index!=args.tokencol:
          if index not in args.to_encode:
            out+='\t'+els[index]
          else:
            out+='\t'+str(extract_rule(els[0],els[index]))
        else:
          out+='\tTOKEN'
      sys.stdout.write(out[1:].encode('utf8')+'\n')
    else:
      sys.stdout.write(line)
