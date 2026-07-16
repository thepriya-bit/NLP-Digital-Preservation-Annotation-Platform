import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="flex items-center justify-between bg-blue-600 px-6 py-4 text-white shadow-md">
      <h1 className="text-xl font-bold">NLP & Digital Preservation</h1>

      <ul className="flex gap-6">
        <li>
          <Link to="/" className="cursor-pointer transition hover:text-gray-200">
            Home
          </Link>
        </li>
        <li>
          <Link to="/dashboard" className="cursor-pointer transition hover:text-gray-200">
            Dashboard
          </Link>
        </li>
        <li>
          <Link to="/login" className="cursor-pointer transition hover:text-gray-200">
            Login
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;