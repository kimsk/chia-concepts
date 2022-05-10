from cmath import sin
import sys
from typing import List, Tuple
sys.path.insert(0, "../../../shared")

from chia.types.blockchain_format.program import Program, SerializedProgram
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.condition_opcodes import ConditionOpcode
from chia.util.hash import std_hash
from chia.util.ints import uint64
from chia.wallet.puzzles import (
    singleton_top_layer
)

from clvm.casts import int_to_bytes

import sim
import singleton_utils

START_AMOUNT: uint64 = uint64(1023)

sim.farm(sim.alice)

launcher_id_1, spend_bundle_1, launcher_coin_spend_1, adapted_puzzle_1 = singleton_utils.create_singleton(sim.alice, START_AMOUNT, [("Group", "A")])

sim.pass_blocks(10)
result_A = sim.push_tx(spend_bundle_1)
print(f'creating eve spend result:\n{result_A}\n')

launcher_id_2, spend_bundle_2, launcher_coin_spend_2, adapted_puzzle_2 = singleton_utils.create_singleton(sim.alice, START_AMOUNT, [("Group", "B")])
result_B = sim.push_tx(spend_bundle_2)
print(f'creating eve spend result:\n{result_B}\n')

launcher_id_3, spend_bundle_3, launcher_coin_spend_3, adapted_puzzle_3 = singleton_utils.create_singleton(sim.alice, START_AMOUNT, [("Group", "C")])
result_C = sim.push_tx(spend_bundle_3)
print(f'creating eve spend result:\n{result_C}\n')

# when the new coin with launcher's puzzle hash (singleton_top_layer.SINGLETON_LAUNCHER) is created and spent
# eff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9

# the observer can look at the solution (using get_puzzle_and_solution) provided to the launcher and see the key value list
# (0x0c0d126c89fc434fbf5ddbf6ad2afd1c5529a9df4f099608c6cd536d753948b2 1023 (("Group" . "A")))
# the singleton child can also be tracked

def get_singleton_by_group(group):
    coin_records = sim.get_coins_records_by_puzzle_hash(singleton_top_layer.SINGLETON_LAUNCHER_HASH) 
    for cr in coin_records:
        coin = cr.coin
        launcher_id = std_hash(
                        coin.parent_coin_info +
                        singleton_top_layer.SINGLETON_LAUNCHER_HASH +
                        int_to_bytes(START_AMOUNT)
        )

        puzz_and_sol = sim.get_puzzle_and_solution(launcher_id, cr.spent_block_index)
        solution: SerializedProgram = puzz_and_sol.solution
        
        solution: Program = solution.to_program()
        # print(disassemble(solution))
        # (0xa1af73b7dc0f246ffb0bd41b4ac8f0253f4c0949bfdd070d52a3be037767baa3 1023 (("Group" . 65)))
        kv = solution.at("rrff")
        # print(disassemble(kv))
        # ("Group" . 67)
        value = kv.as_python()[1].decode('UTF-8')
        # print(value)
        if group == value:
            return coin


# look for group b
group_b = get_singleton_by_group("B")
print(group_b)

is_eve, unspent_singleton = singleton_utils.get_singleton(launcher_id_1)
print(is_eve)
print(unspent_singleton)


spend_bundle_4, coin_spend_4 = singleton_utils.spend_singleton(
    sim.alice,
    launcher_id_1,
    launcher_coin_spend_1,
    adapted_puzzle_1
)
result_D = sim.push_tx(spend_bundle_4)
print(f'spend result:\n{result_D}\n')
is_eve, unspent_singleton = singleton_utils.get_singleton(launcher_id_1)
print(is_eve)
print(unspent_singleton)

sim.end()

