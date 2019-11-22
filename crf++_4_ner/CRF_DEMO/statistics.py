# -*- coding: utf-8 -*-

dir = "../CRF_TEST"

with open("%s/result.txt" % dir, "r") as f:
    sents = [line.strip() for line in f.readlines() if line.strip()]

total = len(sents)
print(total)

count = 0
for sent in sents:
    words = sent.split()
    # print(words)
    if words[-1] == words[-2]:
        count += 1

print("Accuracy: %.4f" %(count/total))
# 0.9706