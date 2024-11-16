import argparse
import asyncio
import logging
from aiopath import AsyncPath
import aioshutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def read_folder(source_folder: AsyncPath, output_folder: AsyncPath):
  if not await source_folder.exists():
    logging.error(f"Source folder {source_folder} does not exist.")
    return

  tasks = []
  async for item in source_folder.rglob("*"):
      if await item.is_file():
          tasks.append(copy_file(item, output_folder))

  await asyncio.gather(*tasks)

async def copy_file(file_path: AsyncPath, output_folder: AsyncPath):
  extension = file_path.suffix.lower()
  target_folder = output_folder / (extension.lstrip('.') if extension else "no_extension")

  try:
    await target_folder.mkdir(parents=True, exist_ok=True)
    target_path = target_folder / file_path.name

    await aioshutil.copy(file_path, target_path)
  except Exception as e:
    logging.error(f"Error copying file {file_path}: {e}")

def parse_arguments():
  parser = argparse.ArgumentParser(description="File sorting")
  parser.add_argument(
    "--source",
    type=str,
    required=True,
    help="Path to the source folder.",
  )
  parser.add_argument(
    "--output",
    type=str,
    required=True,
    help="Path to the output folder.",
  )
  return parser.parse_args()

async def main():
  args = parse_arguments()
  source_folder = AsyncPath(args.source)
  output_folder = AsyncPath(args.output)

  await read_folder(source_folder, output_folder)

if __name__ == "__main__":
  asyncio.run(main())
