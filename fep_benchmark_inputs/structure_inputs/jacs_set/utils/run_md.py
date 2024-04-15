import tempfile
import pathlib
import gufe
from openff.units import unit
import openfe
from openfe.protocols.openmm_md.plain_md_methods import PlainMDProtocol


solv = openfe.SolventComponent()
prot = openfe.ProteinComponent.from_pdb_file('protein.pdb')

settings = openfe.protocols.openmm_md.plain_md_methods.PlainMDProtocol.default_settings()
settings.simulation_settings.equilibration_length_nvt = 0.01 * unit.nanosecond
settings.simulation_settings.equilibration_length = 0.01 * unit.nanosecond
settings.simulation_settings.production_length = 0.01 * unit.nanosecond

protocol = PlainMDProtocol(settings=settings)
system = openfe.ChemicalSystem({'p': prot, 's': solv})
dag = protocol.create(stateA=system, stateB=system, mapping=None)

with tempfile.TemporaryDirectory() as tmpdir:
    workdir = pathlib.Path(tmpdir)
    dagres = gufe.protocols.execute_DAG(
        dag, 
        shared_basedir=workdir,
        scratch_basedir=workdir,
        keep_shared=False,
        n_retries=1,
    )

protres = protocol.gather([dagres])
print(protres.to_dict())
