from qiskit import QuantumCircuit,  ClassicalRegister, QuantumRegister
# Grid Created


class GridCreator:
    def createGrid(n, nr_cycles):

        total_len = 4 * n * n
        edge_len = 2*n

        qreg = QuantumRegister(total_len, name="q")
        init_creg = ClassicalRegister(total_len // 2, name="init")
        cycle1_creg = ClassicalRegister(total_len // 2, name="cycle1")   
        cycle2_creg = ClassicalRegister(total_len // 2, name="cycle2")
        data_creg  = ClassicalRegister(total_len // 2, name="data")

        qc = QuantumCircuit(qreg, init_creg, cycle1_creg, cycle2_creg, data_creg)


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

        ######################################## logical 0 preparation
        classical_id = 0
        for i in range(edge_len):
            for j in range(edge_len):
                if i%2 == 0:
                    if j % 2 == 0:
                        qc.measure(i * edge_len + j, init_creg[classical_id])
                        qc.reset(i * edge_len + j)
                        classical_id += 1

                else:
                    if j % 2 == 1:
                        qc.measure(i * edge_len + j, init_creg[classical_id])
                        qc.reset(i * edge_len + j)
                        classical_id += 1
        
        ######################################### first cycle of correction
        classical_id = 0
        for i in range(edge_len):
            for j in range(edge_len):
                if i%2 == 0:
                    if j % 2 == 0:
                        qc.measure(i * edge_len + j, cycle1_creg[classical_id])
                        qc.reset(i * edge_len + j)
                        classical_id += 1

                else:
                    if j % 2 == 1:
                        qc.measure(i * edge_len + j, cycle1_creg[classical_id])
                        qc.reset(i * edge_len + j)
                        classical_id += 1
        
        ############################################### second cycle of correction
        classical_id = 0
        for i in range(edge_len):
            for j in range(edge_len):
                if i%2 == 0:
                    if j % 2 == 0:
                        qc.measure(i * edge_len + j, cycle2_creg[classical_id])
                        # qc.reset(i * edge_len + j)
                        classical_id += 1

                else:
                    if j % 2 == 1:
                        qc.measure(i * edge_len + j, cycle2_creg[classical_id])
                        # qc.reset(i * edge_len + j)
                        classical_id += 1
        
        ############################################### data qubit measurement
        classical_id = 0
        for i in range(edge_len):
            for j in range(edge_len):
                if i%2 == 0:
                    if j % 2 != 0:
                        qc.measure(i * edge_len + j, data_creg[classical_id])
                        # qc.reset(i * edge_len + j)
                        classical_id += 1

                else:
                    if j % 2 == 0:
                        qc.measure(i * edge_len + j, data_creg[classical_id])
                        # qc.reset(i * edge_len + j)
                        classical_id += 1

        return qc
