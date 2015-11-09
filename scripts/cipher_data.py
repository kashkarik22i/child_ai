#! /usr/bin/env python2.7
from __future__ import unicode_literals

# generic
import os
import os.path

# logging
import logging
logger = logging.getLogger(__name__)

# comman line tool
import click
click.disable_unicode_literals_warning = True

# encryption
import hashlib
import random, struct
from Crypto.Cipher import AES

DEFAULT_FILE_EXTENSION = '.enc'

#################################################
# code related to encrypting was borrowerd from
# http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/
#################################################

def encrypt_file(in_filename, password,
                 out_filename=None, chunksize=64*1024):

    if not out_filename:
        out_filename = in_filename + DEFAULT_FILE_EXTENSION

    iv = b''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    key = hashlib.sha256(password).digest()
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack(b'<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

def decrypt_file(in_filename, password,
                 out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack(b'<Q', infile.read(struct.calcsize(b'Q')))[0]
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

def encrypt_files(filenames, password):
  logger.info("Going to ecrypt {} files".format(len(filenames)))
  for filename in filenames:
    if os.path.isfile(filename): 
      logger.info("Will encrypt file: '{}'".format(filename))
      encrypt_file(filename, password)      
    else:
      logger.warning('File {} does not exist'.format(filename))

def decrypt_files(filenames, password):
  logger.info("Going to decrypt {} files".format(len(filenames)))
  for filename in filenames:
    if not filename.endswith(DEFAULT_FILE_EXTENSION):
      filename += DEFAULT_FILE_EXTENSION
    if os.path.isfile(filename): 
      logger.info("Will decrypt file: '{}'".format(filename))
      decrypt_file(filename, password)      
    else:
      logger.warning('File {} does not exist'.format(filename))

def files_from_list(file_list):
  names = file_list.read().splitlines()
  filtered_names = [name.strip() for name in names if name.strip() != '']
  basepath = os.path.dirname(file_list.name)
  abs_names = [os.path.join(basepath, name) for name in filtered_names]
  return abs_names

################################
# command line parsing
###############################

def validate_options(files, file_list):
  if file_list and files:
    raise click.BadParameter('Cannot use both file list and files')
  elif not file_list and not files:
    raise click.BadParameter('You must provide either file list or files')

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
@click.help_option('-h')
@click.option('--password', '-p', prompt=True, hide_input=True)
@click.option('--file-list', '-l', type=click.File(mode='r', encoding='utf-8'),
              help='File listing files to be encrypted')
@click.argument('files', nargs=-1, metavar='FILES',
                type=click.Path(exists=True, resolve_path=False))
def encrypt(password, file_list, files):
  validate_options(files, file_list)
  files = files if files else files_from_list(file_list)
  encrypt_files(files, password)
 
#DECRYPT
@click.command(help='Decrypt any number of files')
@click.help_option('-h')
@click.option('--password', '-p', prompt=True, hide_input=True)
@click.option('--file-list', '-l', type=click.File(mode='r', encoding='utf-8'),
              help='File listing files to be decrypted (without .enc extension)')
@click.argument('files', nargs=-1, metavar='FILES',
                type=click.Path(exists=True, resolve_path=False))
def decrypt(password, file_list, files):
  validate_options(files, file_list)
  files = files if files else files_from_list(file_list)
  decrypt_files(files, password)

# putting arguments together    
cli.add_command(encrypt)
cli.add_command(decrypt)

if __name__ == "__main__":
  cli()
