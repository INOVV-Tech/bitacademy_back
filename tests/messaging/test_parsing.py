import json
import pytest

from tests.common import load_app_env

load_app_env()

from src.shared.utils.time import now_timestamp_milli

from src.shared.messaging.parser import parse_input_msg

TEST_INPUT_CONTENT = '💰 Valor do farm: Gratuito ⛓️ Rede: Testnets na carteira Portal. 🏫 Funding: $42.5M (Coinbase Ventures, OKX Ventures, Arrington Capital) Sobre o projeto: Portal to Bitcoin é um protocolo que permite trocas cross-chain de Bitcoin sem necessidade de bridges ou tokens wrapped. O projeto introduz o BitScaler, uma tecnologia que melhora a escalabilidade do Bitcoin sem modificar sua base. O time conta com veteranos do setor desde 2011 e já levantou $42.5 milhões em funding. OBS: O airdrop será distribuído depois dessa testnet, onde os usuários podem ganhar Litenodes e obter recompensas perpétuas da rede. ✅ Tutorial: Como participar do airdrop Portal to Bitcoin Acesse o testnet do Portal to Bitcoin: Visite o Portal to Bitcoin Testnet: https://portaltobitcoin.bonusblock.io/?r=uDekFFsF Conecte sua carteira compatível. Gere seu link de referência. Instale a extensão Portal to Bitcoin: Acesse a Chrome Web Store: https://chromewebstore.google.com/detail/portal-dex/ieldiilncjhfkalnemgjbffmpomcaigi Clique em “Adicionar ao Chrome” e instale a extensão. Complete missões no testnet: Vá até o Dashboard de Missões: https://portaltobitcoin.bonusblock.io/quests Veja as tarefas disponíveis e suas recompensas em sparks. Complete as missões e acompanhe sua posição no ranking. Participe dos Epochs (fases semanais do testnet): A cada semana, uma nova fase (Epoch) será aberta. Complete as missões especiais de cada Epoch. Mantenha uma participação consistente para subir no ranking. Distribuição do Token: Supply Total: 8.4 bilhões de tokens Supply de Emissões: 4.9 bilhões de tokens (58.3%) Alocação para Litenodes: 5% das emissões por Epoch Número de Litenodes: Apenas 21.000 posições disponíveis Dicas para maximizar sua posição: Entre o quanto antes para acumular mais sparks. Complete todas as missões disponíveis. Mantenha-se ativo em todas as seis Epochs. Compartilhe seu link de referência para aumentar seus pontos. Fique de olho em novas oportunidades e atualizações. ❓ Dúvidas que talvez vocês tenham: Quanto tempo dura o testnet? O testnet terá seis Epochs (semanas), onde os participantes podem competir por posições nos Litenodes. Se eu perder um Epoch, ainda posso participar? Sim, mas sua pontuação será menor. Você ainda pode competir nas fases seguintes. Como as recompensas serão distribuídas? Os operadores de Litenode receberão uma parte da alocação de 5% por Epoch e continuarão ganhando recompensas da rede. Conclusão: O testnet do Portal to Bitcoin é uma oportunidade de fazer parte do ecossistema DeFi do Bitcoin e garantir uma posição como Litenode Operator, com recompensas perpétuas. Como há apenas 21.000 vagas, este airdrop é bastante competitivo. Fique ligado na aba de Notícias Exclusivas do nosso Discord fechado para novas interações e snapshots! Bom farm!'

class Test_MessagingParsing:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))

    @pytest.mark.skip(reason='Done')
    def test_input_msg(self):
        msg = parse_input_msg(TEST_INPUT_CONTENT)

        assert msg != None

        self.print_data(msg.to_dict())

    @pytest.mark.skip(reason='Done')
    def test_performance(self):
        ini = now_timestamp_milli()

        for i in range(0, 1):
            parse_input_msg(TEST_INPUT_CONTENT)
        
        diff = now_timestamp_milli() - ini

        print(f'Time diff (ms) = {diff}')