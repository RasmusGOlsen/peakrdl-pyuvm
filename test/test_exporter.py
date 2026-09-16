import importlib.util
import os
import sys
import tempfile
from importlib.resources import as_file, files

import pytest
from systemrdl import RDLCompileError, RDLCompiler

from peakrdl_pyuvm.exporter import PyUVMExporter

from . import resources


@pytest.fixture(scope="session")
def model():
    rdlc = RDLCompiler()
#    for udp in ALL_UDPS:
#        rdlc.register_udp(udp)
    try:
        with as_file(files(resources).joinpath("TinyALUreg.rdl")) as rdlfile:
            rdlc.compile_file(rdlfile)
        root = rdlc.elaborate()
    except RDLCompileError as err:
        raise SystemError from err
    fd, filepath = tempfile.mkstemp(suffix=".py")
    os.close(fd)
    exporter = PyUVMExporter()
    exporter.export(root, filepath)
    module_name = "generated_model"
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_exporter(model):
    bar0 = model.BAR0("bar0")
    bar0.build()
    bar0.lock_model()

    assert len(bar0.get_registers()) == 57
    assert len(bar0.get_maps()) == 1
    assert len(bar0.get_blocks()) == 3
    assert bar0.get_name() == "bar0"
