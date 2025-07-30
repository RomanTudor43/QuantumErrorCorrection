from qiskit import QuantumCircuit,  ClassicalRegister, QuantumRegister
# Grid Created


class GridCreator:
    def createGrid(n):

        total_len = 4 * n * n
        edge_len = 2*n
        qc = QuantumCircuit(total_len)

        parity_changer = 0

        for i in range(edge_len):
            for j in range(edge_len):
                if i%2 == 0:
                    if j % 2 == 0:
                        qc.cx( (i * edge_len) + (j + 1) % edge_len, i * edge_len + j)
                        qc.cx(i * edge_len + (j - 1) % edge_len, i * edge_len + j)
                        qc.cx((i * edge_len + j + edge_len) % total_len , i * edge_len + j)
                        qc.cx((i * edge_len + j - edge_len) % total_len , i * edge_len + j)

                else:
                    if j % 2 == 1:
                        qc.h( i * edge_len + j)
                        qc.cx( i * edge_len + j, i * edge_len + (j + 1) % edge_len )
                        qc.cx( i * edge_len + j, i * edge_len + (j - 1) % edge_len)
                        qc.cx( i * edge_len + j ,   (i * edge_len + j + edge_len) % total_len )
                        qc.cx( i * edge_len + j , (i * edge_len + j - edge_len) % total_len )
                        qc.h( i * edge_len + j)

        return qc
