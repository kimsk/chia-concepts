import { ChiaDaemon, loadUIConfig } from 'chia-daemon';

const daemon = new ChiaDaemon(loadUIConfig(), 'my-chia-app');
const connected = await daemon.connect();
if (connected) {
    const state = await daemon.services.full_node.get_blockchain_state();
    console.log(state);
    const coin_record = await daemon.services.full_node.get_coin_record_by_name({ name: '0xacbd6d8a8d787cc44715e4fdcf68f77cb1e2247f297302e90d3e031824244d7e' });
    console.log(coin_record)
}
process.exit()