# -*- coding: utf-8 -*-
"""
.. codeauthor:: Jaume Bonet <jaume.bonet@gmail.com>

.. affiliation::
    Laboratory of Protein Design and Immunoengineering <lpdi.epfl.ch>
    Bruno Correia <bruno.correia@epfl.ch>
"""
# Standard Libraries
import os

# External Libraries
import matplotlib.pyplot as plt
import pytest

# This Library
from rstoolbox.io import parse_rosetta_fragments
from rstoolbox.plot import plot_fragment_profiles


class TestFragments( object ):
    """
    Test usage of the FragmentFrame component.
    """
    def setup_method( self, method ):
        self.dirpath = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.frag3 = os.path.join(self.dirpath, 'wauto.200.3mers.gz')
        self.frag3q = os.path.join(self.dirpath, 'wauto.200.3mers.qual.gz')
        self.frag9 = os.path.join(self.dirpath, 'wauto.200.9mers.gz')
        self.frag9q = os.path.join(self.dirpath, 'wauto.200.9mers.qual.gz')

    @pytest.mark.mpl_image_compare(baseline_dir='../baseline_images',
                                   filename='plot_fragment_profiles.png')
    def test_quality_plot( self ):
        df3 = parse_rosetta_fragments(self.frag3)
        df9 = parse_rosetta_fragments(self.frag9)
        # auto-load
        df3 = df3.add_quality_measure(None)
        # load target quality file
        with pytest.raises(ValueError):
            df9 = df9.add_quality_measure(self.frag3q)
        df9 = df9.add_quality_measure(self.frag9q)

        assert df3.is_comparable(df9) is False

        assert 'rmsd' in df3
        assert 'rmsd' in df9

        consensus_seq = df9.select_quantile().quick_consensus_sequence()
        consensus_sse = df9.select_quantile().quick_consensus_secondary_structure()

        assert consensus_seq == "KIPVPVVVNGKIVAVVVVPPENLEEALLEALKELGLIKDPEEVKAVVVSPDGRLELSF"
        assert consensus_sse == "EEEEEEEELLEEEEEEEELLLLHHHHHHHHHHHHLLLLLLLLLLEEEEELLLEEEEEE"

        fig = plt.figure(figsize=(25, 10))
        plot_fragment_profiles(fig, df3, df9, consensus_seq, consensus_sse)
        plt.tight_layout()
        return fig

    def test_frequency_matrices_and_networks( self ):
        df3 = parse_rosetta_fragments(self.frag3)
        df9 = parse_rosetta_fragments(self.frag9)
        # auto-load
        df3 = df3.add_quality_measure(None)
        # load target quality file
        df9 = df9.add_quality_measure(self.frag9q)

        matrix = df3.select_quantile(0.1).make_sequence_matrix()
        assert matrix.min().min() == -9

        matrix = df9.select_quantile(0.1).make_sequence_matrix(frequency=True)
        G = df9.select_quantile(0.1).make_per_position_frequency_network()
        Gf = df9.select_quantile(0.1).make_frequency_network()

        assert matrix.shape == (58, 20)
        assert G.number_of_edges() > Gf.number_of_edges()

        value = 1 - G.get_edge_data("0X", "1A")['weight']
        assert matrix["A"].values[0] == pytest.approx(value)

        n = 6
        target = str(n + 1) + "R"
        for aa in list("ARNDCQEGHILKMFPSTWYV"):
            origin = str(n) + aa
            if origin in G:
                value = 1 - G.get_edge_data(origin, target)['weight']
                assert matrix["R"].values[n] == pytest.approx(value)
