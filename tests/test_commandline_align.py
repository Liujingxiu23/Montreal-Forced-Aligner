import os
import pytest

from montreal_forced_aligner.command_line.align import run_align_corpus, load_basic_align
from montreal_forced_aligner.command_line.mfa import parser

from montreal_forced_aligner.exceptions import PronunciationAcousticMismatchError


def assert_export_exist(old_directory, new_directory):
    for root, dirs, files in os.walk(old_directory):
        new_root = root.replace(old_directory, new_directory)
        for d in dirs:
            assert (os.path.exists(os.path.join(new_root, d)))
        for f in files:
            if not f.endswith('.wav'):
                continue
            new_f = f.replace('.wav', '.TextGrid')
            assert (os.path.exists(os.path.join(new_root, new_f)))


def test_align_arguments(basic_corpus_dir, sick_dict_path, generated_dir, large_dataset_dictionary, temp_dir,
                         english_acoustic_model):

    command = ['align', basic_corpus_dir, large_dataset_dictionary, 'english', os.path.join(generated_dir, 'basic_output'),
               '-t', temp_dir, '-q', '--clean', '-d', '--disable_sat']
    args, unknown_args = parser.parse_known_args(command)
    align_config = load_basic_align()
    assert not align_config.disable_sat
    if unknown_args:
        align_config.update_from_args(unknown_args)
    assert align_config.disable_sat

#@pytest.mark.skip(reason='Optimization')
def test_align_basic(basic_corpus_dir, sick_dict_path, generated_dir, large_dataset_dictionary, temp_dir,
                     basic_align_config, english_acoustic_model):
    command = ['align', basic_corpus_dir, sick_dict_path, 'english', os.path.join(generated_dir, 'basic_output'),
               '-t', temp_dir, '-c', basic_align_config, '-q', '--clean', '-d']
    args, unknown = parser.parse_known_args(command)
    with pytest.raises(PronunciationAcousticMismatchError):
        run_align_corpus(args, unknown)

    command = ['align', basic_corpus_dir, large_dataset_dictionary, 'english', os.path.join(generated_dir, 'basic_output'),
               '-t', temp_dir, '-c', basic_align_config, '-q', '--clean', '-d']
    args, unknown = parser.parse_known_args(command)
    run_align_corpus(args, unknown)

def test_align_stereo(stereo_corpus_dir, sick_dict_path, generated_dir, large_dataset_dictionary, temp_dir,
                     basic_align_config, english_acoustic_model):

    command = ['align', stereo_corpus_dir, large_dataset_dictionary, 'english', os.path.join(generated_dir, 'stereo_output'),
               '-t', temp_dir, '-c', basic_align_config, '-q', '--clean', '-d']
    args, unknown = parser.parse_known_args(command)
    run_align_corpus(args, unknown)

