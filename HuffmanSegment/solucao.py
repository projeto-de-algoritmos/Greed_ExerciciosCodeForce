import heapq

SQRT = 500
MAX = 1_000_01

class Query:
    def __init__(self, l, r, id):
        self.l = l
        self.r = r
        self.id = id
        self.buck = l // SQRT

    def __lt__(self, other):
        if self.buck != other.buck:
            return self.buck < other.buck
        return self.r < other.r

def optimize_huffman_coding(n, ar, m, queries):
    answers = [0] * m

    def add(val, freq, bucket_freq, geqRoot):
        if freq[val] >= SQRT:
            freq[val] += 1
        elif freq[val] == SQRT - 1:
            bucket_freq[SQRT - 1] -= 1
            freq[val] += 1
            geqRoot.add(val)
        else:
            bucket_freq[freq[val]] -= 1
            freq[val] += 1
            bucket_freq[freq[val]] += 1

    def rem(val, freq, bucket_freq, geqRoot):
        if freq[val] < SQRT:
            bucket_freq[freq[val]] -= 1
            freq[val] -= 1
            bucket_freq[freq[val]] += 1
        elif freq[val] == SQRT:
            geqRoot.remove(val)
            bucket_freq[SQRT - 1] += 1
            freq[val] -= 1
        else:
            freq[val] -= 1

    qs = [Query(l - 1, r - 1, i) for i, (l, r) in enumerate(queries)]
    qs.sort()

    l = 0
    r = -1
    bucket_freq = [0] * SQRT
    freq = [0] * MAX
    geqRoot = set()
    bucket_freq[0] = n

    for qq in range(m):
        q = qs[qq]
        if q.l == q.r:
            continue

        while r < q.r:
            r += 1
            add(ar[r], freq, bucket_freq, geqRoot)
        while l > q.l:
            l -= 1
            add(ar[l], freq, bucket_freq, geqRoot)
        while r > q.r:
            rem(ar[r], freq, bucket_freq, geqRoot)
            r -= 1
        while l < q.l:
            rem(ar[l], freq, bucket_freq, geqRoot)
            l += 1

        res = 0
        pq = [freq[ii] for ii in geqRoot]
        pq.sort()

        curFreq = bucket_freq[:]

        leftover = -1
        for i in range(1, SQRT):
            here = curFreq[i]
            if here == 0:
                continue

            if leftover != -1:
                newval = leftover + i
                res += newval

                if newval >= SQRT:
                    pq.append(newval)
                else:
                    curFreq[newval] += 1

                leftover = -1
                here -= 1

            if here & 1 == 1:
                leftover = i
                here -= 1

            res += i * here
            newval = i * 2

            if newval >= SQRT:
                pq.extend([newval] * (here >> 1))
            else:
                curFreq[newval] += here >> 1

        if leftover != -1:
            pq.append(leftover)

        heapq.heapify(pq)

        while len(pq) > 1:
            a = heapq.heappop(pq)
            b = heapq.heappop(pq)
            res += a + b
            heapq.heappush(pq, a + b)

        answers[q.id] = res

    return answers

n = int(input())
ar = list(map(lambda x: int(x) - 1, input().split()))
m = int(input())
queries = [tuple(map(int, input().split())) for _ in range(m)]

output = optimize_huffman_coding(n, ar, m, queries)

for ans in output:
    print(ans)