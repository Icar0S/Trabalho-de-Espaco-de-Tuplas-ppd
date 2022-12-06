# Trabalho-de-Espaco-de-Tuplas-ppd

Desenvolver um sistema de Gerenciamento de Ambientes Multinuvens
com as seguintes características:
1. Pode haver múltiplas nuvens (nuvem1, nuvem2, nuvem3, …).
Podem haver múltiplos hosts (host1, host2, host3, …). Também
podem haver múltiplas VMs (vm1, vm2, vm3, …) e múltiplos
processos (p1, p2, p3, …).
2. Uma Nuvem pode ter vários Hosts, que, por sua vez, pode possuir
várias VMs e uma VM pode ter vários Processos. Não podem haver
nomes repetidos dentro de um mesmo contêiner.
3. Processos podem trocar mensagens entre si desde que estejam na
mesma VM.
4. Deve ser possível criar e remover nuvens, hosts, VMs e processos.
Nuvens, hosts e VMs só podem ser removidos se estiverem vazios.
5. Deve ser possível migrar hosts entre nuvens, VMs entre hosts e
processos entre VMs. Deve ser solicitado a renomeação de
elementos caso existam outros com o mesmo nome no mesmo
contêiner.
