from qiskit import QuantumCircuit,  ClassicalRegister, QuantumRegister
# Grid Created


class GridCreator:
    def createGrid(n, nr_cycles):

        edge_len = 2*n + 1

        total_len = edge_len * edge_len

        qreg = QuantumRegister(total_len, name="q")
        init_creg = ClassicalRegister(total_len // 2, name="init")
        cycle1_creg = ClassicalRegister(total_len // 2, name="cycle1")   
        cycle2_creg = ClassicalRegister(total_len // 2, name="cycle2")
        data_creg  = ClassicalRegister(total_len // 2 + 1, name="data")
        # data_creg  = ClassicalRegister(2, name="data")

        qc = QuantumCircuit(qreg, init_creg, cycle1_creg, cycle2_creg, data_creg)


        ####################################### Logical 1 prep
        # for i in range(edge_len):
        #     for j in range(edge_len):
        #         if i%2 == 0:
        #             if j % 2 != 0:
        #                 qc.x(i * edge_len + j)

        #         else:
        #             if j % 2 == 0:
        #                 qc.x(i * edge_len + j)

        


        for i in range(edge_len):
            for j in range(edge_len):
                if i % 2 != 0 and j % 2 == 0:
                    # Odd row, even col — apply H and connect to neighbors if they exist
                    qc.h(i * edge_len + j)
                    if j + 1 < edge_len:  # right neighbor
                        qc.cx(i * edge_len + j, i * edge_len + (j + 1))
                    if j - 1 >= 0:  # left neighbor
                        qc.cx(i * edge_len + j, i * edge_len + (j - 1))
                    if i + 1 < edge_len:  # below
                        qc.cx(i * edge_len + j, (i + 1) * edge_len + j)
                    if i - 1 >= 0:  # above
                        qc.cx(i * edge_len + j, (i - 1) * edge_len + j)
                    qc.h(i * edge_len + j)

                elif i % 2 == 0 and j % 2 == 1:
                    # Even row, odd col — connect neighbors if they exist
                    if j + 1 < edge_len:  # right
                        qc.cx(i * edge_len + (j + 1), i * edge_len + j)
                    if j - 1 >= 0:  # left
                        qc.cx(i * edge_len + (j - 1), i * edge_len + j)
                    if i + 1 < edge_len:  # below
                        qc.cx((i + 1) * edge_len + j, i * edge_len + j)
                    if i - 1 >= 0:  # above
                        qc.cx((i - 1) * edge_len + j, i * edge_len + j)



        ######################################## logical state preparation
        classical_id = 0
        for i in range(edge_len):
            for j in range(edge_len):
                # Odd row, even col  OR  Even row, odd col
                if (i % 2 == 1 and j % 2 == 0) or (i % 2 == 0 and j % 2 == 1):
                    qc.measure(i * edge_len + j, init_creg[classical_id])
                    qc.reset(i * edge_len + j)
                    classical_id += 1

        
        ######################################### first cycle of correction
        classical_id = 0
        for i in range(edge_len):
            for j in range(edge_len):
                # Odd row, even col  OR  Even row, odd col
                if (i % 2 == 1 and j % 2 == 0) or (i % 2 == 0 and j % 2 == 1):
                    qc.measure(i * edge_len + j, cycle1_creg[classical_id])
                    qc.reset(i * edge_len + j)
                    classical_id += 1



        ############################################### Apply logic X


        # for i in range(edge_len):
        #     if i % 2 == 0:
        #         qc.x(edge_len + i)
                        
        
        ############################################### second cycle of correction
        classical_id = 0
        for i in range(edge_len):
            for j in range(edge_len):
                # Odd row, even col  OR  Even row, odd col
                if (i % 2 == 1 and j % 2 == 0) or (i % 2 == 0 and j % 2 == 1):
                    qc.measure(i * edge_len + j, cycle2_creg[classical_id])
                    qc.reset(i * edge_len + j)
                    classical_id += 1
        
        ############################################### Apply logic X


        # for i in range(edge_len):
        #     if i % 2 == 0:
        #         qc.x(edge_len + i)
        
        ############################################### data qubit measurement
        classical_id = 0
        for i in range(edge_len):
            for j in range(edge_len):
                # Odd row, even col  OR  Even row, odd col
                if i % 2 == j % 2:
                    qc.measure(i * edge_len + j, data_creg[classical_id])
                    qc.reset(i * edge_len + j)
                    classical_id += 1
        # classical_id = 0
        # qc.measure(9, data_creg[classical_id])
        # classical_id += 1
        # qc.measure(6, data_creg[classical_id])
        # classical_id += 1


        return qc
