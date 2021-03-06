# -*- coding: utf-8 -*-
"""
.. codeauthor:: Jaume Bonet <jaume.bonet@gmail.com>
.. codeauthor:: Fabian Sesterhenn <sesterhenn.fabian@gmail.com>

.. affiliation::
    Laboratory of Protein Design and Immunoengineering <lpdi.epfl.ch>
    Bruno Correia <bruno.correia@epfl.ch>

.. func:: read_SPR
.. func:: read_fastq
"""
# Standard Libraries
import gzip

# External Libraries
import pandas as pd

# This Library
import rstoolbox.components as rc

__all__ = ['read_SPR', 'read_fastq']


def read_SPR( filename ):
    """Reads **Surface Plasmon Resonance** data.

    The input data should be a comma-separated file with two types of header, one for raw data::

        Run 1; Ch 1; Cy 6; RefSub; name; conc=0.0585_X ,...

    And one for fitted data::

        Run 1; Ch 1; Cy 16; RefSub; 1kx8_d02; conc=60 fitted curve_X ,...

    each ``conc`` condition will have a ``_X`` and ``_Y`` value.

    This seems to be a pretty standard format as output from the machine.

    :param str filename: Input file.

    :return: :class:`pandas.DataFrame` with ``MultiIndex``.

    .. seealso::
        :func:`.plot_SPR`

    .. rubric:: Example

    .. ipython::

        In [1]: from rstoolbox.io import read_SPR
           ...: import pandas as pd
           ...: pd.set_option('display.width', 1000)
           ...: df = read_SPR("../rstoolbox/tests/data/spr_data.csv.gz")
           ...: df.head(2)
    """
    df = pd.read_csv(filename, low_memory=False).dropna(how='all')
    df.columns = [_.split(';')[-1].replace('conc=', '') for _ in df.columns]
    condition = ['raw' if 'fitted' not in _ else 'fitted' for _ in df.columns]
    concentration = [_.split('_')[0].replace('fitted curve', '').strip() for _ in df.columns]
    axis = [_.split('_')[-1].strip() for _ in df.columns]
    newidx = [(x, y, z) for x, y, z in zip(condition, concentration, axis)]
    df.columns = pd.MultiIndex.from_tuples(newidx)
    df.columns.names = ['data', 'concentration', 'axis']
    df.index = range(0, df.shape[0])
    return df.astype('float64')


def read_fastq( filename, seqID='A'):
    """Reads a FASTQ file and stores the ID together with the sequence.

    The default generated :class:`.DesignFrame` will contain two columns:

    ====================  ===================================================
    Column Name            Data Content
    ====================  ===================================================
    **description**        Sequence identifier.
    **sequence_<chain>**   Sequence content.
    ====================  ===================================================

    :param str filename: FASTQ filename.
    :param str seqID: |seqID_param|

    :return: :class:`.DesignFrame`

    .. rubric:: Example

    .. ipython::

        In [1]: from rstoolbox.io import read_fastq
           ...: import pandas as pd
           ...: pd.set_option('display.width', 1000)
           ...: df = read_fastq("../rstoolbox/tests/data/cdk2_rand_001.fasq.gz")
           ...: df.head(8)
    """
    # Empty array to store tuples of ID & sequence information
    fastq = []
    idq = []

    # Create a file handle for parsing
    is_gz = filename.endswith('gz')
    fastq_file = gzip.open(filename) if is_gz else open(filename)
    for line in fastq_file:
        line = line.decode('utf8') if is_gz else line
        if line.startswith('@'):
            idq.append(str(line.split(':')[0].split(';')[0][1:]))
        if '@' in line or '+' in line or any(c.islower() for c in line):
            continue
        if len(line) == 0:
            continue
        fastq.append(str(line.strip()))
    return rc.DesignFrame({'description': idq, 'sequence_{}'.format(seqID): fastq})
