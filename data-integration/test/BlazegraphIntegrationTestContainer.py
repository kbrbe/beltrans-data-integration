import docker as dockerlib

docker = dockerlib.from_env()

class BlazegraphIntegrationTestContainer:

  def __init__(self, imageName, hostName):
    self._imageName = imageName
    self._hostName = hostName

  def __enter__(self):
    print(f'build image {self._imageName}...')
    self._image = docker.images.build(path='./blazegraph', tag=self._imageName)
    print(f'run container ...')
    self._container = docker.containers.run(image=self._imageName, detach=True, hostname=self._hostName, ports={"8080": "8080"})
    return self._container

  def __exit__(self, *args):
    self._container.kill()
    self._container.remove()

  def wait(self):
    self._container.wait()

if __name__ == '__main__':
  with BlazegraphIntegrationTestContainer("data-integration_blazegraph-test") as blazegraph:  
    try:
      for line in blazegraph.logs(stream=True):
        print(f'{line}')
    except InterruptedError as e:
      pass
