async def format_response(text):
    if len(text) > 2000:
        chunks = []
        current_chunk = ""
        code_block = False
        code_block_lang = ""
        lines = text.split('\n')

        for line in lines:
            if line.strip().startswith('```'):
                if not code_block:
                    code_block = True
                    code_block_lang = line.strip()[3:].strip()
                else:
                    code_block = False

            if len(current_chunk) + len(line) + 1 > 2000:
                if code_block:
                    current_chunk += '```\n'
                chunks.append(current_chunk.strip())
                current_chunk = ""
                if code_block:
                    current_chunk += f'```{code_block_lang}\n'

            current_chunk += line + '\n'

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
    else:
        return [text]