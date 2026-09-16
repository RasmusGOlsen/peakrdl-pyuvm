# peakrdl-pyuvm

[PeakRDL](https://peakrdl.readthedocs.io/) plugin that generates a [pyuvm] register
model from SystemRDL.

The generated output is a single Python module containing `pyuvm` register classes
that can be instantiated and used in any UVM-based Python testbench.

[pyuvm]: https://github.com/pyuvm/pyuvm

## Installation

```bash
pip install peakrdl-pyuvm
```

The PeakRDL host CLI is optional — install it with the `cli` extra if you want to
use the `peakrdl pyuvm` command:

```bash
pip install "peakrdl-pyuvm[cli]"
```

## Usage

Export a register model:

```bash
peakrdl pyuvm my_design.rdl -o my_ral.py
```

Use the generated module in your testbench:

```python
from my_ral import BAR0

block = BAR0("bar0")
block.build()
block.lock_model()

# Iterate registers
for reg in block.get_registers():
    print(reg.get_name())

# Write a field
block.ALU0.SRC.data0.write(0xFF)
```

The generated module contains one class per register, one class per register block,
and one top-level block class. All classes inherit from `pyuvm.uvm_reg_block` /
`pyuvm.uvm_reg`.
