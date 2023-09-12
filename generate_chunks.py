def generate_chunks(amount, max_chunk, iterable_pairs_len):
    chunks = []
    for i in range(amount // max_chunk):
        chunk = []
        for j in range(max_chunk):
            chunk.append(iterable_pairs_len)
            iterable_pairs_len -= 1
        chunks.append(chunk)
    return chunks
