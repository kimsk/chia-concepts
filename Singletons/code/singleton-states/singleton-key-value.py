import sys
from typing import List, Tuple
sys.path.insert(0, "../../../shared")

import sim
import singleton_utils


sim.farm(sim.alice)

comment: List[Tuple[str, str]] = [("Group", "A")]
launcher_id_1, spend_bundle = singleton_utils.create_singleton(sim.alice, comment)

sim.pass_blocks(10)
result = sim.push_tx(spend_bundle)
print(f'creating eve spend result:\n{result}\n')

comment: List[Tuple[str, str]] = [("Group", "B")]
launcher_id_2, spend_bundle = singleton_utils.create_singleton(sim.alice, comment)
result = sim.push_tx(spend_bundle)
print(f'creating eve spend result:\n{result}\n')

comment: List[Tuple[str, str]] = [("Group", "C")]
launcher_id_3, spend_bundle = singleton_utils.create_singleton(sim.alice, comment)
result = sim.push_tx(spend_bundle)
print(f'creating eve spend result:\n{result}\n')

# look for group b
group_b = singleton_utils.get_singleton("B")
print(group_b)


# when the new coin with launcher's puzzle hash (singleton_top_layer.SINGLETON_LAUNCHER) is created and spent
# eff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9

# the observer can look at the solution (using get_puzzle_and_solution) provided to the launcher and see the key value list
# (0x0c0d126c89fc434fbf5ddbf6ad2afd1c5529a9df4f099608c6cd536d753948b2 1023 (("Group" . 1) ("Number" . 7)))

# the singleton child can also be tracked

# coin = sim.get_coin_record_by_coin_id(launcher_id)
# print(coin)

# {'coin': {'amount': 1023,
#           'parent_coin_info': '0x12d7b8c1654f82f2330059abc28e3240e863450706de7fdc518026f393f68bba',
#           'puzzle_hash': '0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9'},
#  'coinbase': False,
#  'confirmed_block_index': 12,
#  'spent_block_index': 12,
#  'timestamp': 1}
# puzz_and_sol = sim.get_puzzle_and_solution(launcher_id, 12)
# print(puzz_and_sol)

# 'coin': {'amount': 1023,
#           'parent_coin_info': '0x12d7b8c1654f82f2330059abc28e3240e863450706de7fdc518026f393f68bba',
#           'puzzle_hash': '0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9'},
#  'puzzle_reveal': '0xff02ffff01ff04ffff04ff04ffff04ff05ffff04ff0bff80808080ffff04ffff04ff0affff04ffff02ff0effff04ff02ffff04ffff04ff05ffff04ff0bffff04ff17ff80808080ff80808080ff808080ff808080ffff04ffff01ff33ff3cff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff0effff04ff02ffff04ff09ff80808080ffff02ff0effff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080',
#  'solution': '0xffa0a1af73b7dc0f246ffb0bd41b4ac8f0253f4c0949bfdd070d52a3be037767baa3ff8203ffffffff8547726f757001ffff864e756d626572078080'}

# ❯ opd ffa0a1af73b7dc0f246ffb0bd41b4ac8f0253f4c0949bfdd070d52a3be037767baa3ff8203ffffffff8547726f757001ffff864e756d626572078080
# (0xa1af73b7dc0f246ffb0bd41b4ac8f0253f4c0949bfdd070d52a3be037767baa3 1023 (("Group" . 1) ("Number" . 7)))

# coin_records = sim.get_coin_records_by_parent_ids([launcher_id])
# print(coin_records[0].coin)

# {'amount': 1023,
#  'parent_coin_info': '0x6a4ba7e394f8d346deafcda74b26bcad649ed0cb691d7172b14970c4cf47a570',
#  'puzzle_hash': '0xa1af73b7dc0f246ffb0bd41b4ac8f0253f4c0949bfdd070d52a3be037767baa3'}

sim.end()

