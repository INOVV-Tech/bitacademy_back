from typing import List, Any

def batchfy(values: List[Any], batch_size: int) -> List[List[Any]]:
    batchs = [[]]
    
    for value in values:
        batchs[-1].append(value)

        if len(batchs[-1]) == batch_size:
            batchs.append([])

    if len(batchs[-1]) == 0:
        batchs = batchs[:-1]

    return batchs