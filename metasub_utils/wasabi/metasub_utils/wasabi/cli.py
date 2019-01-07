"""CLI for commands to be related to wasabi."""

import click

from .wasabi_bucket import WasabiBucket


@click.group()
def wasabi():
    pass


@wasabi.command('list')
@click.argument('profile_name', default='wasabi')
def cli_list_wasabi_files(profile_name):
    """List all files in the wasabi bucket."""
    wasabi_bucket = WasabiBucket(profile_name=profile_name)
    for file_key in wasabi_bucket.list_files():
        print(file_key)


@wasabi.command('status')
@click.option('-v/-c', '--verbose/--concise', default=False)
@click.option('-p', '--profile-name', default='wasabi')
def cli_wasabi_status(verbose, profile_name):
    """Print a status report."""
    wasabi_bucket = WasabiBucket(profile_name=profile_name)
    samples_with_reads = {
        '_'.join(raw_reads[0].split('/')[-1].split('_')[:3])
        for raw_reads in wasabi_bucket.list_raw(grouped=True)
    }
    samples_with_contigs = {
        contig_file.split('/')[-2].split('.metaspades')[0]
        for contig_file in wasabi_bucket.list_contigs()
    }
    all_samples = samples_with_reads |  samples_with_contigs
    samples_with_both = samples_with_reads & samples_with_contigs
    samples_with_just_reads = samples_with_reads - samples_with_both
    samples_with_just_contigs = samples_with_contigs - samples_with_both
    click.echo(f'{len(all_samples)} total samples')
    click.echo(f'{len(samples_with_both)} samples with reads and contigs')
    click.echo(f'{len(samples_with_just_reads)} samples with just reads')
    click.echo(f'{len(samples_with_just_contigs)} samples with just contigs')
    if verbose:
        for sample in samples_with_both:
            print(f'{sample} BOTH')
        for sample in samples_with_just_reads:
            print(f'{sample} JUST_READS')
        for sample in samples_with_just_contigs:
            print(f'{sample} JUST_CONTIGS')


@wasabi.command('list-unassembled')
@click.argument('profile_name', default='wasabi')
def cli_list_unassembled_data(profile_name):
    """List unassembled data in the wasabi bucket."""
    wasabi_bucket = WasabiBucket(profile_name=profile_name)
    for file_key in wasabi_bucket.list_unassembled_data():
        print(file_key)


@wasabi.command('list-raw-reads')
@click.option('-g/-s', '--grouped/--single', default=False)
@click.option('-p', '--profile-name', default='wasabi')
@click.option('-c', '--city-name', default=None)
@click.option('-s', '--sample-names', default=None, type=click.File('r'))
def cli_list_raw_reads(grouped, profile_name, city_name, sample_names):
    """List unassembled data in the wasabi bucket."""
    wasabi_bucket = WasabiBucket(profile_name=profile_name)
    if sample_names:
        sample_names = {line.strip() for line in sample_names}
    file_keys = wasabi_bucket.list_raw(
        city_name=city_name, grouped=grouped, sample_names=sample_names
    )
    for file_key in file_keys:
        if grouped:
            file_key = ' '.join(file_key)
        print(file_key)


@wasabi.command('download-raw-reads')
@click.option('-d/-w', '--dryrun/--wetrun', default=True)
@click.option('-p', '--profile-name', default='wasabi')
@click.option('-c', '--city-name', default=None)
@click.option('-s', '--sample-names', default=None, type=click.File('r'))
@click.argument('target_dir', default='data')
def cli_download_raw_data(dryrun, profile_name, city_name, sample_names, target_dir):
    """Download raw sequencing data, from a particular city if specified."""
    wasabi_bucket = WasabiBucket(profile_name=profile_name)
    if sample_names:
        sample_names = {line.strip() for line in sample_names}
    wasabi_bucket.download_raw(
        sample_names=sample_names,
        city_name=city_name,
        target_dir=target_dir,
        dryrun=dryrun,
    )
    wasabi_bucket.close()


@wasabi.command('download-unassembled-data')
@click.option('-d/-w', '--dryrun/--wetrun', default=True)
@click.option('-p', '--profile-name', default='wasabi')
@click.argument('target_dir', default='data')
def cli_download_unassembled_data(dryrun, profile_name, target_dir):
    """Download data without contig files from wasabi."""
    wasabi_bucket = WasabiBucket(profile_name=profile_name)
    wasabi_bucket.download_unassembled_data(
        target_dir=target_dir,
        dryrun=dryrun,
    )
    wasabi_bucket.close()


@wasabi.command('download-contigs')
@click.option('-d/-w', '--dryrun/--wetrun', default=True)
@click.option('-p', '--profile-name', default='wasabi')
@click.argument('target_dir', default='assemblies')
def cli_download_contig_files(dryrun, profile_name, target_dir):
    """Download contig files from wasabi."""
    wasabi_bucket = WasabiBucket(profile_name=profile_name)
    wasabi_bucket.download_contigs(
        target_dir=target_dir,
        dryrun=dryrun,
    )
    wasabi_bucket.close()
