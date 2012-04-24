import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Paint;
import java.awt.Stroke;
import java.util.Iterator;
import java.util.Scanner;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;

import javax.swing.JFrame;

import org.apache.commons.collections15.Transformer;

import edu.uci.ics.jung.algorithms.layout.CircleLayout;
import edu.uci.ics.jung.algorithms.layout.Layout;
import edu.uci.ics.jung.graph.Graph;
import edu.uci.ics.jung.graph.UndirectedSparseMultigraph;
import edu.uci.ics.jung.graph.DirectedSparseMultigraph;
import edu.uci.ics.jung.visualization.BasicVisualizationServer;
import edu.uci.ics.jung.visualization.decorators.ToStringLabeller;


public class ChetMonitor {
	
	protected JFrame frame = new JFrame("Monitor");
	
	public static final int Width = 600;
	public static final int Height = 400;
	public static final int LayoutUpdateDelay = 250;
	
	private ConcurrentHashMap<String, Vertex> vertices = new ConcurrentHashMap<String, Vertex>();
	
	private ConcurrentLinkedQueue<Edge> edgeList = new ConcurrentLinkedQueue<Edge>();
	
	private Scanner scan = new Scanner(System.in);
	
	/**
	 * The amount of milliseconds for which an edge appears on the graph.
	 */
	public static final int EdgeDelay = 500;
	
	/**
	 * Create a new monitor and start the updater threads.
	 */
	public ChetMonitor() {
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setVisible(true);

		Thread t = new Thread(new StaticLayoutUpdater(), "StaticLayoutUpdater");
		t.start();
		
		mainloop();
		
		
		//Thread p = new Thread(new VertexPruner(this), "VertexPruner");
		//p.start();
	}
	
	public void mainloop(){
		while(true){
			String nextLine = scan.next();
			String[] arr = nextLine.split("#");
			if (arr[0].equals("New")){
				Vertex toadd = new Vertex(arr[1], arr[2]);
				vertices.put(arr[2], toadd);
			}else if(arr[0].equals("Dead")){
				vertices.remove(arr[1]);
			}else if(arr[0].equals("Msg")){
				if(arr.length == 4){
					Edge toadd = new Edge(vertices.get(arr[1]), vertices.get(arr[2]), arr[3]);
					edgeList.add(toadd);
				}else if(arr.length == 5){
					Edge toadd = new Edge(
							vertices.get(arr[1]), 
							vertices.get(arr[2]),
							arr[3],
							Float.parseFloat(arr[4]));
				}
			}else if(arr[0].equals("Load")){
				if(arr.length==3){
					String name = arr[1];
					int load = Integer.parseInt(arr[2]);
					//setsize
				}
			}
		}
	}
	
	/**
	 * Transform the given edge (by name) so that its color matches others that were generated from
	 * the same protocol.
	 */
	private final Transformer<String, Paint> edgeGossipTransformer = new Transformer<String, Paint>() {
		@Override
		public Paint transform(String s) {
			if (s.startsWith("ndp")) {
				return Color.BLUE;
			} else if (s.startsWith("mdp") || s.startsWith("mr")) {
				/*
				 * Dark green, calculated from:
				 * 
				 * http://www.squarebox.co.uk/users/rolf/download/ColourWheel/
				 */
				return Color.getHSBColor((float) 0.3, (float) 0.9, (float) 0.6);
			} else if (s.startsWith("udp") || s.startsWith("ur")) {
				return Color.RED;
			} else {
				return Color.BLACK;
			}
		}
	};

	
	
	/**
	 * Transform the given edge (based on name) so that certain commands (replication) have thicker
	 * edges than normal communication for that protocol.
	 */
	private final Transformer<String, Stroke> edgeCommandTransformer = new Transformer<String, Stroke>() {
		@Override
		public Stroke transform(String s) {
			Stroke bs;
			if (s.startsWith("mr")) {
				float dash[] = {10.0f};
				bs = new BasicStroke(9.0f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER, 10.0f, dash, 0.0f);
			} else if (s.startsWith("ur")) {
				bs = new BasicStroke(9.0f);
			} else {
				bs = new BasicStroke(1.0f);
			}
			return bs;
		}
	};
	
	/**
	 * Transform the given edge (based on name) so that certain commands (replication) have thicker
	 * edges than normal communication for that protocol.
	 */
	private final Transformer<String, Stroke> vertexStrokeTransformer = new Transformer<String, Stroke>() {
		@Override
		public Stroke transform(String s) {
			Stroke bs;
			if (s.startsWith("mr")) {
				float dash[] = {10.0f};
				bs = new BasicStroke(9.0f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER, 10.0f, dash, 0.0f);
			} else if (s.startsWith("ur")) {
				bs = new BasicStroke(9.0f);
			} else {
				bs = new BasicStroke(1.0f);
			}
			return bs;
		}
	};
	

	
	/**
	 * Run through all the nodes and edges in the map and create graph edges and vertices for them.
	 * 
	 * @return The filled-in graph.
	 */
	public Graph<String, String> getGraph() {
		Graph<String, String> graph = new DirectedSparseMultigraph<String, String>();
		
		Iterator<String> vi = vertices.keySet().iterator();
		while (vi.hasNext()){
			graph.addVertex(vertices.get(vi.next()).getName());
		}

		while(edgeList.size()>0){
			Edge toAdd = edgeList.poll();
			graph.addEdge(toAdd.getCode(), toAdd.getA().getName(), toAdd.getB().getName());
		}
		return graph;
	}
	
	/**
	 * Retrieve the "viewer" (visualization handler) for the provided graph.
	 * 
	 * @param graph The graph to visualize.
	 * @return The viewer.
	 */
	public BasicVisualizationServer<String, String> getViewer(Graph<String, String> graph) {
		Dimension d = new Dimension(Width, Height);
		Layout<String, String> layout = new CircleLayout<String, String>(graph);
		layout.setSize(d);
		layout.initialize();
		BasicVisualizationServer<String, String> vv = new BasicVisualizationServer<String, String>(layout);
		vv.setPreferredSize(d);
		vv.getRenderContext().setVertexLabelTransformer(new ToStringLabeller<String>());
		vv.getRenderContext().setEdgeDrawPaintTransformer(edgeGossipTransformer);
		vv.getRenderContext().setEdgeStrokeTransformer(edgeCommandTransformer);
		vv.getRenderContext().setVertexStrokeTransformer(vertexStrokeTransformer);
		return vv;
	}
		
	
	/**
	 * Updates the graph when it contains a static layout.
	 *
	 * @author Josh Endries (josh@endries.org)
	 *
	 */
	protected class StaticLayoutUpdater implements Runnable {
		private boolean running = false;
		
		@Override
		public void run() {
			running = true;
			while (running) {
				Graph<String, String> graph = getGraph();
				BasicVisualizationServer<String, String> vv = getViewer(graph);
				frame.getContentPane().removeAll();
				frame.getContentPane().add(vv);
				frame.pack();
				
				try {
					Thread.sleep(LayoutUpdateDelay);
				} catch (InterruptedException e) {
					running = false;
				}
			}
		}
	}
	
	
	public static void main(String[] args){
		ChetMonitor monitor = new ChetMonitor();
		//SystemInListener snl = new SystemInListener();
		//Thread t = new Thread(ucl, "UDP Command Handler");
		//t.start();
	}

}