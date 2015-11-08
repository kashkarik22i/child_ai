#! /usr/bin/env python2.7
from __future__ import unicode_literals

# logging
import logging
logger = logging.getLogger(__name__)

# comman line tool
import click
click.disable_unicode_literals_warning = True

# encryption
import hashlib
import os, random, struct
from Crypto.Cipher import AES

#################################################
# code related to encrypting was borrowerd from
# http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/
#################################################

def encrypt_file(password, in_filename,
                 out_filename=None, chunksize=64*1024):

    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    key = hashlib.sha256(password).digest()
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

def decrypt_file(password, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        key = hashlib.sha256(password).digest()
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)

################################
# command line parsing
###############################

# CLI
@click.group()
@click.help_option('-h')
@click.option('--log', default='info',
              type=click.Choice(['info', 'debug', 'error', 'warninig']),
              help='log level')
def cli(log):
  logging.basicConfig()
  logger.setLevel(log.upper())

#ENCRYPT
@click.command(help='Encrypt any number of files')
@click.option('--password', '-p', prompt=True, hide_input=True)
@click.argument('files', nargs=-1,
                type=click.Path(exists=True, resolve_path=False))
def encrypt(password, files):
  logger.info("Going to ecrypt some files")
  for f in files:
    logger.info("Will encrypt file: '{}'".format(f))

#DECRYPT
@click.command(help='Decrypt any number of files')
@click.option('--password', '-p', prompt=True, hide_input=True)
@click.argument('files', nargs=-1,
                type=click.Path(exists=True, resolve_path=False))
def decrypt(password, files):
  logger.info("Going to decrypt some files")
  for f in files:
    logger.info("Will decrypt file: '{}'".format(f))

cli.add_command(encrypt)
cli.add_command(decrypt)

if __name__ == "__main__":
  cli()
