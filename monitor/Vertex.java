
public class Vertex {

	private String name;
	private String uid;
	private String type;
	
	public Vertex(String name, String uid){
		this.name = name;
		this.uid = uid;
	}
	
	public String getName(){
		return this.name;
	}
	public String getUid(){
		return this.uid;
	}
	public String getType(){
		return this.type;
	}
}
