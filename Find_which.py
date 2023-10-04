import cv2
import numpy as np
import os

import time
import pymiere
from pymiere import wrappers
from pymiere import Time

overlay_types_list = ["no_video_1", "no_video_2", "no_video_3", "no_video_4", "no_video_5", "no_video_6", "small_1",
                      "small_2", "small_3", "small_4", "small_5", "small_6", "medium_1", "medium_2", "medium_3",
                      "medium_4", "medium_5", "medium_6", "large_1", "large_2", "large_3", "large_4", "large_5",
                      "large_6"]


def create_overlays_png(overlay_background_path, folder_path, edit_name):

  overlay_background = cv2.imread(overlay_background_path)
  overlays_alpha = []

  # Check if the folder exists
  if os.path.exists(folder_path):

    for overlay_template in overlay_types_list:
      overlay = cv2.imread(overlay_template, cv2.IMREAD_GRAYSCALE)
      overlay_img = cv2.addWeighted(overlay_background, 1.0, overlay, 1.0, 0)
      overlay_path = folder_path + "/" + str(overlay_template) + edit_name
      cv2.imwrite(overlay_path, overlay_img)
      overlays_alpha.append(overlay_path)

    return overlays_alpha

  else:
    print(f"The folder {folder_path} does not exist.")

    return []


def count_boxes_in_image():
  pass

def find_which_overlay(image, current_overlay, overlay_template):
  if np.mean(image + current_overlay) < 10:
    return current_overlay
  else:
    for overlay in overlay_template:
      if np.mean(image + overlay) < 10:
        return overlay
      else:
        continue
  return []


def find_overlays_placement(overlay_template):
  """Detects black boxes in a grayscale video frame by frame."""

  # Open the video file.
  video_capture = cv2.VideoCapture("video.mp4")

  start_frame = 1
  end_frame = 1
  overlays = []
  current_overlay = overlay_template[0]
  # Loop over the video frames.
  current_frame_number = 0
  while True:
    # Capture the next frame.
    ret, frame = video_capture.read()
    current_frame_number += 1
    # If there is no more frame, then break out of the loop.
    if not ret:
      break

    # Detect black boxes in the frame.
    temp_overlay = find_which_overlay(frame, current_overlay, overlay_template)
    if overlay != temp_overlay:
      overlay = temp_overlay
      end_frame = current_frame_number
      overlays.append([overlay, (start_frame, end_frame)])
      start_frame = current_frame_number + 1


  # Release the video capture.
  video_capture.release()


def pr_edits(overlay_name, overlay_infos):
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

  start_time = Time()
  start_time.seconds = overlay_infos[0]

  end_time = Time()
  end_time.seconds = overlay_infos[1]

  # Select the first video clip in the Timeline

  item_name = "sdf.png"

  names = [list(project.rootItem.children)[i].name for i in range(0, len(list(project.rootItem.children)))]

  clips[0].setSelected(True, True)
  item = project.rootItem.children[list(names).index(item_name)]
  project.activeSequence.videoTracks[1].insertClip(item, 0)
  clips_names = [list(project.activeSequence.videoTracks[1].clips)[i].name for i in range(0, len(list(project.activeSequence.videoTracks[1].clips)))]

  project.activeSequence.videoTracks[1].clips[clips_names.index(item_name)].start = start_time
  project.activeSequence.videoTracks[1].clips[clips_names.index(item_name)].end = end_time



def main(overlay_path):
  overlays = find_overlays_png(overlay_path)
  pr_edits(overlay_name, overlay_infos)


if __name__ == "__main__":
  main()