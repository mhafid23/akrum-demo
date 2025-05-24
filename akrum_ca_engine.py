
def rule30_ca_key_stream(seed: str, length: int) -> str:
    rule30 = {
        '111': '0', '110': '0', '101': '0', '100': '1',
        '011': '1', '010': '1', '001': '1', '000': '0'
    }
    state = list(seed)
    output = state.copy()
    n = len(state)

    while len(output) < length:
        next_state = []
        for i in range(n):
            left = state[i - 1] if i > 0 else state[-1]
            center = state[i]
            right = state[i + 1] if i < n - 1 else state[0]
            next_state.append(rule30[left + center + right])
        output.extend(next_state)
        state = next_state

    return ''.join(output[:length])
