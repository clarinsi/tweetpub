#!/usr/bin/python

# you can obtain the lower values by creating an app at https://apps.twitter.com
CONSUMER_KEY=''
CONSUMER_SECRET=''
ACCESS_TOKEN=''
ACCESS_TOKEN_SECRET=''

import sys
import argparse
import tweepy
import re
from time import sleep,time

text_start_re=re.compile(r'^<text ')
tid_re=re.compile(r'id="tid.(.+?)"')
text_end_re=re.compile(r'^</text')

auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
api=tweepy.API(auth)

def apply_rule(token,rule):
  rule=list(eval(rule))
  return rule[1]+token[rule[0]:len(token)-rule[2]]+rule[3]

def construct_tweets(tweets):
  statuses=None
  for i in range(3):
    try:
      statuses=api.statuses_lookup(tweets.keys())
      break
    except Exception as e:
      sys.stderr.write('Problem in communicating with API. Will try in 5...\n')
      sys.stderr.write(str(e)+'\n')
      sleep(5)
  if statuses==None:
    sys.stderr.write('Could not get data...\n')
  else:
    for status in statuses:
      for line in tweets[status.id]:
        els=line[:-1].decode('utf8').split('\t')
        if len(els)==args.ncol:
          offset=els[args.offsetcol].split('-')
          token=status.text[int(offset[0])-1:int(offset[1])]
          out=''
          for index in range(len(els)):
            if index==args.tokencol:
              out+='\t'+token
            elif index not in args.to_decode:
              out+='\t'+els[index]
            else:
              out+='\t'+apply_rule(token,els[index])
          sys.stdout.write(out[1:].encode('utf8')+'\n')
        else:
          sys.stdout.write(line)

if __name__=='__main__':
  parser=argparse.ArgumentParser(description='Decoder of annotated tweet collections from a shareable format. Twitter API authentication information must be provided at the beginning of the script before usage.')
  parser.add_argument('--ncol',help='number of columns in lines representing tokens',type=int,required=True)
  parser.add_argument('--offsetcol',help='index of column containing the offset',type=int,required=True)
  parser.add_argument('--tokencol',help='index of column containing the token, default is 1',type=int,default=1)
  parser.add_argument('--to_decode',help='indices of columns to be decoded from the token value',type=int,nargs='+')
  args=parser.parse_args()
  args.offsetcol-=1
  args.tokencol-=1
  if args.to_decode!=None:
    for i in range(len(args.to_decode)):
      args.to_decode[i]-=1
  tweets={}
  tweet=None
  start=0
  for line in sys.stdin:
    if text_start_re.search(line)!=None:
      tid=int(tid_re.search(line).group(1))
      tweet=[line]
      continue
    if tweet==None:
      sys.stdout.write(line)
      continue
    tweet.append(line)
    if text_end_re.search(line)!=None:
      tweets[tid]=tweet[:]
      tweet=None
      if len(tweets)==100:
        if time()-start<16:
          sleep(max(0,16-(time()-start)))
        start=time()
        construct_tweets(tweets)
        tweets={}
  if time()-start<16:
    sleep(max(0,16-(time()-start)))
  construct_tweets(tweets)
