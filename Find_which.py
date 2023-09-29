import cv2
import numpy as np
import os

import time
import pymiere
from pymiere import wrappers
from pymiere import Time


def find_overlays_png(folder_path):

  # Check if the folder exists
  if os.path.exists(folder_path):
    # Use listdir to get a list of items in the folder
    items = os.listdir(folder_path)

    # You can filter out specific items if needed, for example, only files:
    files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]

    # Or only directories:
    directories = [item for item in items if os.path.isdir(os.path.join(folder_path, item))]

    # Print the list of items, files, and directories
    print("All items in the folder:")
    print(items)

    print("\nOnly files in the folder:")
    print(files)

    print("\nOnly directories in the folder:")
    print(directories)

    return files
  else:
    print(f"The folder {folder_path} does not exist.")

    return []


def count_boxes_in_image():
  pass


def find_overlays_placement():
  """Detects black boxes in a grayscale video frame by frame."""

  # Open the video file.
  video_capture = cv2.VideoCapture("video.mp4")

  overlay = find_which_overlay()
  start_frame = 1
  end_frame = 1
  overlays = []

  # Loop over the video frames.
  while True:
    # Capture the next frame.
    ret, frame = video_capture.read()

    # If there is no more frame, then break out of the loop.
    if not ret:
      break

    # Detect black boxes in the frame.
    temp_overlay = find_which_overlay(frame)
    if overlay != temp_overlay:
      overlay = temp_overlay
      end_frame = current_frame_number
      overlays.append([overlay, (start_frame, end_frame)])
      start_frame = current_frame_number + 1

  # Release the video capture.
  video_capture.release()


def pr_edits():
  # Check for an open project
  project_opened, sequence_active = wrappers.check_active_sequence(crash=False)
  if not project_opened:
    raise ValueError("please open a project")

  project = pymiere.objects.app.project

  # Open Sequences in Premiere Pro if none are active
  if not sequence_active:
    sequences = wrappers.list_sequences()
    for seq in sequences:
      project.openSequence(sequenceID=seq.sequenceID)
    # Set the first Sequence in the list as the active Sequence
    project.activeSequence = sequences[0]

  # List all videos clips in the active Sequence
  clips = wrappers.list_video(project.activeSequence)

  # Convert timebase in ticks per second to Frame Per Second (FPS)
  fps = 1 / (float(project.activeSequence.timebase) / wrappers.TICKS_PER_SECONDS)
  print("Sequence as a framerate of {} fps".format(fps))


  overlays_infos = [20, 40]

  start_time = Time()
  start_time.seconds = overlays_infos[0]

  end_time = Time()
  end_time.seconds = overlays_infos[1]

  # Select the first video clip in the Timeline

  item_name = "sdf.png"

  names = [list(project.rootItem.children)[i].name for i in range(0, len(list(project.rootItem.children)))]

  clips[0].setSelected(True, True)
  item = project.rootItem.children[list(names).index(item_name)]
  project.activeSequence.videoTracks[1].insertClip(item, 0)
  clips_names = [list(project.activeSequence.videoTracks[1].clips)[i].name for i in range(0, len(list(project.activeSequence.videoTracks[1].clips)))]

  project.activeSequence.videoTracks[1].clips[clips_names.index(item_name)].start = start_time
  project.activeSequence.videoTracks[1].clips[clips_names.index(item_name)].end = end_time




def main():
  # overlays_images = find_overlays_png(path)
  # overlays_infos = find_overlays_placement()
  pr_edits()





if __name__ == "__main__":
  main()