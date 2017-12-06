export default function listenServer(setFlowData) {

  const port = 4444;
  const host = '0.0.0.0'
  const url = `ws://${host}:${port}/ws`;

  const ws = new WebSocket(url);

  ws.onopen = event => {
    console.log('WebSocket opened');
  };

  ws.onerror = event => {
    console.log('WebSocket error');
  };

  ws.onclose = event => {
    console.log('WebSocket closed');
  };

  ws.onmessage = event => {
      setFlowData(JSON.parse(event.data));
  };

}
